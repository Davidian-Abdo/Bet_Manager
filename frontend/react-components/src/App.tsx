import React from 'react';
import SimpleCADViewer from './components/SimpleCADViewer';
import './App.css';

declare global {
  interface Window {
    STREAMLIT_CONFIG: {
      projectId: number;
      token: string;
      backendUrl: string;
      userRole: string;
      userName: string;
    };
  }
}

const App: React.FC = () => {
  const config = window.STREAMLIT_CONFIG;

  if (!config) {
    return (
      <div style={{ 
        padding: '40px', 
        textAlign: 'center',
        backgroundColor: '#f8d7da',
        color: '#721c24',
        borderRadius: '8px',
        margin: '20px'
      }}>
        <h2>❌ Erreur de Configuration</h2>
        <p>Aucune configuration fournie par Streamlit.</p>
        <p>Veuillez recharger la page.</p>
      </div>
    );
  }

  return (
    <div className="App">
      <SimpleCADViewer
        projectId={config.projectId}
        token={config.token}
        backendUrl={config.backendUrl}
        userRole={config.userRole}
        userName={config.userName}
      />
    </div>
  );
};

export default App;