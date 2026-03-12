from fastapi import APIRouter, Depends, HTTPException, Query, Header
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Investigation, Evidence
from app.reporting import (
    ReportGenerator, AnalysisGenerator, ReportFormat
)
from fastapi.responses import StreamingResponse
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/{investigation_id}/summary")
async def get_investigation_summary(
    investigation_id: str,
    db: Session = Depends(get_db),
    authorization: str = Header(None)
):
    """Отримати резюме розслідування"""
    investigation = db.query(Investigation).filter(
        Investigation.id == investigation_id
    ).first()
    
    if not investigation:
        raise HTTPException(status_code=404, detail="Investigation not found")
    
    evidence = db.query(Evidence).filter(
        Evidence.investigation_id == investigation_id
    ).all()
    
    return {
        "investigation": {
            "id": investigation.id,
            "title": investigation.title,
            "target": investigation.target_identifier,
            "status": investigation.status,
            "created_at": investigation.created_at.isoformat()
        },
        "evidence_count": len(evidence),
        "tools_used": list(set(e.source for e in evidence))
    }

@router.post("/{investigation_id}/generate-report")
async def generate_investigation_report(
    investigation_id: str,
    format: str = Query("json"),
    include_analysis: bool = Query(True),
    db: Session = Depends(get_db),
    authorization: str = Header(None)
):
    """Згенерувати ЗАГАЛЬНИЙ ЗВІТ розслідування"""
    
    investigation = db.query(Investigation).filter(
        Investigation.id == investigation_id
    ).first()
    
    if not investigation:
        raise HTTPException(status_code=404, detail="Investigation not found")
    
    evidence_list = db.query(Evidence).filter(
        Evidence.investigation_id == investigation_id
    ).all()
    
    # Ініціалізувати звіт
    report = ReportGenerator(investigation_id)
    
    # Додати виконавчий звіт
    report.add_executive_summary(
        target=investigation.target_identifier,
        findings=investigation.description or "OSINT дослідження",
        risk_level="UNKNOWN"
    )
    
    # Парсити докази за категоріями
    social_profiles = []
    infrastructure = []
    breaches = []
    geolocation = []
    financial = {}
    
    for evidence in evidence_list:
        try:
            data = json.loads(evidence.data) if isinstance(evidence.data, str) else evidence.data
        except:
            data = {"raw": evidence.data}
        
        if evidence.source in ["maigret", "sherlock"]:
            social_profiles.append(data)
        
        elif evidence.source in ["shodan", "censys"]:
            infrastructure.append(data)
        
        elif evidence.source in ["geospy", "google_earth"]:
            geolocation.append(data)
        
        elif evidence.source in ["dehashed", "haveibeenpwned"]:
            breaches.append(data)
        
        elif evidence.source in ["opensanctions", "youcontrol"]:
            financial = data
    
    # Додати результати
    if social_profiles:
        report.add_osint_search_results(investigation.target_identifier, social_profiles)
    
    if infrastructure:
        report.add_network_intelligence(infrastructure)
    
    if geolocation:
        report.add_geolocation_data(geolocation)
    
    if financial:
        report.add_financial_data(financial)
    
    # Додати аналіз загроз
    if include_analysis:
        threat_analysis = AnalysisGenerator.generate_threat_assessment({
            "social_profiles": social_profiles,
            "infrastructure": infrastructure,
            "breaches": breaches,
            "sanctions_hits": bool(financial.get("sanctions_status") != "Clear")
        })
        
        report.add_threat_assessment(threat_analysis["threats"])
        recommendations = AnalysisGenerator.generate_recommendations(threat_analysis)
        report.add_recommendations(recommendations)
    
    # Додати докази
    report.add_evidence([
        {
            "source": e.source,
            "data": e.data,
            "timestamp": e.created_at.isoformat() if hasattr(e.created_at, 'isoformat') else str(e.created_at)
        }
        for e in evidence_list
    ])
    
    # Додати висновки
    report.add_conclusion(
        f"Дослідження завершено {datetime.now().strftime('%d.%m.%Y %H:%M')}. "
        f"Всього використано {len(report.report_data['metadata']['tools_used'])} інструментів. "
        f"Збережено {len(evidence_list)} доказів з хешуванням для юридичної значущості."
    )
    
    # Експортувати у вказаному форматі
    report_data = report.generate_json_report()
    
    if format.lower() == "json":
        return report_data
    
    elif format.lower() == "html":
        html_content = report.generate_html_report()
        return StreamingResponse(
            iter([html_content]),
            media_type="text/html",
            headers={"Content-Disposition": f"attachment; filename=report_{investigation_id}.html"}
        )
    
    elif format.lower() == "markdown":
        md_content = report.generate_markdown_report()
        return StreamingResponse(
            iter([md_content]),
            media_type="text/markdown",
            headers={"Content-Disposition": f"attachment; filename=report_{investigation_id}.md"}
        )
    
    elif format.lower() == "csv":
        csv_content = report.generate_csv_report()
        return StreamingResponse(
            iter([csv_content]),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=report_{investigation_id}.csv"}
        )
    
    else:
        return {
            "error": f"Unsupported format: {format}",
            "supported": ["json", "html", "markdown", "csv"]
        }

@router.get("/{investigation_id}/analysis")
async def get_threat_analysis(
    investigation_id: str,
    db: Session = Depends(get_db),
    authorization: str = Header(None)
):
    """Отримати аналіз загроз та ризиків"""
    
    investigation = db.query(Investigation).filter(
        Investigation.id == investigation_id
    ).first()
    
    if not investigation:
        raise HTTPException(status_code=404, detail="Investigation not found")
    
    evidence_list = db.query(Evidence).filter(
        Evidence.investigation_id == investigation_id
    ).all()
    
    # Підготувати дані для аналізу
    analysis_data = {
        "social_profiles": [],
        "infrastructure": [],
        "breaches": [],
        "sanctions_hits": False
    }
    
    for evidence in evidence_list:
        try:
            data = json.loads(evidence.data) if isinstance(evidence.data, str) else evidence.data
        except:
            data = {}
        
        if evidence.source in ["maigret", "sherlock"]:
            analysis_data["social_profiles"].append(data)
        elif evidence.source in ["shodan", "censys"]:
            analysis_data["infrastructure"].append(data)
        elif evidence.source in ["dehashed", "haveibeenpwned"]:
            analysis_data["breaches"].append(data)
        elif evidence.source == "opensanctions":
            analysis_data["sanctions_hits"] = True
    
    threat_assessment = AnalysisGenerator.generate_threat_assessment(analysis_data)
    recommendations = AnalysisGenerator.generate_recommendations(threat_assessment)
    
    return {
        "investigation_id": investigation_id,
        "threat_assessment": threat_assessment,
        "recommendations": recommendations,
        "analysis_timestamp": datetime.now().isoformat()
    }

@router.get("/{investigation_id}/statistics")
async def get_investigation_statistics(
    investigation_id: str,
    db: Session = Depends(get_db),
    authorization: str = Header(None)
):
    """Отримати статистику розслідування"""
    
    investigation = db.query(Investigation).filter(
        Investigation.id == investigation_id
    ).first()
    
    if not investigation:
        raise HTTPException(status_code=404, detail="Investigation not found")
    
    evidence_list = db.query(Evidence).filter(
        Evidence.investigation_id == investigation_id
    ).all()
    
    # Статистика за інструментами
    tools_used = {}
    for evidence in evidence_list:
        tools_used[evidence.source] = tools_used.get(evidence.source, 0) + 1
    
    # Статистика за категоріями розвідки
    categories = {
        "GEOINT": 0,
        "SIGINT": 0,
        "SOCMINT": 0,
        "FININT": 0,
        "DARKWEB": 0,
        "CONTACT": 0,
        "AI": 0,
        "TRANSPORT": 0,
        "OTHER": 0
    }
    
    category_mapping = {
        "geospy": "GEOINT",
        "google_earth": "GEOINT",
        "shodan": "SIGINT",
        "censys": "SIGINT",
        "maigret": "SOCMINT",
        "sherlock": "SOCMINT",
        "opensanctions": "FININT",
        "youcontrol": "FININT",
        "dehashed": "DARKWEB",
        "haveibeenpwned": "DARKWEB",
        "hunter": "CONTACT",
        "phoneinfoga": "CONTACT"
    }
    
    for source in tools_used.keys():
        category = category_mapping.get(source, "OTHER")
        categories[category] += tools_used[source]
    
    return {
        "investigation_id": investigation_id,
        "evidence_count": len(evidence_list),
        "tools_used": tools_used,
        "categories": categories,
        "status": investigation.status,
        "created_at": investigation.created_at.isoformat(),
        "data_quality_score": min(len(evidence_list) / 10 * 100, 100) if evidence_list else 0
    }
