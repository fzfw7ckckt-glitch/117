import React from 'react';
import { AppBar, Toolbar, Typography, Container, Box } from '@mui/material';

interface LayoutProps {
  children: React.ReactNode;
}

export default function Layout({ children }: LayoutProps) {
  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            🛡️ OSINT Platform 2026
          </Typography>
          <Typography variant="body2">Beta</Typography>
        </Toolbar>
      </AppBar>
      <Container component="main" sx={{ flexGrow: 1 }}>
        {children}
      </Container>
      <Box component="footer" sx={{ py: 2, backgroundColor: '#f5f5f5', mt: 4 }}>
        <Container>
          <Typography variant="body2" color="textSecondary" align="center">
            © 2024 OSINT Platform. All rights reserved.
          </Typography>
        </Container>
      </Box>
    </Box>
  );
}
