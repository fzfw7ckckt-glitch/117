import React, { useEffect, useState } from 'react';
import { Container, Typography, Grid, Card, CardContent, Chip, Box } from '@mui/material';
import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface Tool {
  name: string;
  category: string;
  description: string;
}

const categoryColors: { [key: string]: string } = {
  SOCMINT: '#FF6B6B',
  SIGINT: '#4ECDC4',
  GEOINT: '#45B7D1',
  FININT: '#FFA07A',
  HUMINT: '#98D8C8',
};

export default function ToolsPage() {
  const [tools, setTools] = useState<{ [key: string]: Tool }>({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchTools = async () => {
      try {
        const response = await axios.get(`${API_URL}/tools/`);
        setTools(response.data.tools);
      } catch (error) {
        console.error('Failed to fetch tools:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchTools();
  }, []);

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h3" component="h1" gutterBottom>
        📋 OSINT Tools Catalog
      </Typography>
      <Typography variant="subtitle1" color="textSecondary" paragraph>
        {Object.keys(tools).length}+ integrated intelligence gathering tools
      </Typography>

      {loading ? (
        <Typography>Loading tools...</Typography>
      ) : (
        <Grid container spacing={2}>
          {Object.entries(tools).map(([key, tool]) => (
            <Grid item xs={12} sm={6} md={4} key={key}>
              <Card sx={{ height: '100%' }}>
                <CardContent>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                    <Typography variant="h6">{tool.name}</Typography>
                    <Chip
                      label={tool.category}
                      size="small"
                      sx={{
                        backgroundColor: categoryColors[tool.category] || '#999',
                        color: 'white',
                      }}
                    />
                  </Box>
                  <Typography variant="body2" color="textSecondary">
                    {tool.description}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}
    </Container>
  );
}
