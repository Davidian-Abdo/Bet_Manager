import React, { useRef, useState } from 'react';

interface SimpleCADViewerProps {
  projectId: number;
  token: string;
  backendUrl: string;
  userRole: string;
  userName: string;
}

const SimpleCADViewer: React.FC<SimpleCADViewerProps> = ({
  projectId,
  userRole,
  userName
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [isDrawing, setIsDrawing] = useState(false);
  const [hasAccess, setHasAccess] = useState(userRole === 'admin' || userRole === 'engineer');
  const [currentEditor, setCurrentEditor] = useState<string | null>(
    userRole === 'admin' || userRole === 'engineer' ? userName : null
  );

  const startDrawing = (e: React.MouseEvent<HTMLCanvasElement>) => {
    if (!hasAccess || !canvasRef.current) return;
    
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    ctx.beginPath();
    ctx.moveTo(x, y);
    ctx.strokeStyle = '#000000';
    ctx.lineWidth = 2;
    setIsDrawing(true);
  };

  const draw = (e: React.MouseEvent<HTMLCanvasElement>) => {
    if (!isDrawing || !hasAccess || !canvasRef.current) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    ctx.lineTo(x, y);
    ctx.stroke();
  };

  const stopDrawing = () => {
    setIsDrawing(false);
  };

  const clearCanvas = () => {
    if (!canvasRef.current) return;
    const ctx = canvasRef.current.getContext('2d');
    if (ctx) {
      ctx.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height);
    }
  };

  const requestAccess = () => {
    setHasAccess(true);
    setCurrentEditor(userName);
  };

  const releaseAccess = () => {
    setHasAccess(false);
    setCurrentEditor(null);
  };

  return (
    <div style={{ 
      padding: '20px', 
      fontFamily: 'Arial, sans-serif',
      maxWidth: '900px',
      margin: '0 auto'
    }}>
      {/* Header */}
      <div style={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center',
        marginBottom: '20px',
        padding: '15px',
        backgroundColor: '#f8f9fa',
        borderRadius: '8px',
        border: '1px solid #dee2e6'
      }}>
        <div>
          <h2 style={{ margin: 0, color: '#333' }}>🖊️ Visionneuse CAD</h2>
          <p style={{ margin: '5px 0 0 0', color: '#666' }}>
            <strong>Éditeur:</strong> {currentEditor || 'Aucun'} | 
            <strong> Statut:</strong> {hasAccess ? '🟢 Éditeur' : '🔴 Observateur'} |
            <strong> Projet:</strong> #{projectId}
          </p>
        </div>
        
        <div style={{ display: 'flex', gap: '10px' }}>
          {!hasAccess && (userRole === 'engineer' || userRole === 'admin') && (
            <button 
              onClick={requestAccess}
              style={{
                padding: '10px 20px',
                backgroundColor: '#28a745',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer',
                fontWeight: 'bold'
              }}
            >
              📝 Demander Accès
            </button>
          )}
          
          {hasAccess && (
            <button 
              onClick={releaseAccess}
              style={{
                padding: '10px 20px',
                backgroundColor: '#dc3545',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer',
                fontWeight: 'bold'
              }}
            >
              🔓 Libérer Accès
            </button>
          )}
          
          <button 
            onClick={clearCanvas}
            style={{
              padding: '10px 20px',
              backgroundColor: '#6c757d',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
              fontWeight: 'bold'
            }}
          >
            🧹 Effacer
          </button>
        </div>
      </div>

      {/* Canvas */}
      <div style={{ position: 'relative' }}>
        <canvas
          ref={canvasRef}
          width={800}
          height={500}
          onMouseDown={startDrawing}
          onMouseMove={draw}
          onMouseUp={stopDrawing}
          onMouseLeave={stopDrawing}
          style={{
            border: '2px solid #495057',
            backgroundColor: '#ffffff',
            cursor: hasAccess ? 'crosshair' : 'not-allowed',
            borderRadius: '4px',
            display: 'block',
            margin: '0 auto',
            boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)'
          }}
        />
        
        {!hasAccess && (
          <div style={{
            position: 'absolute',
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            textAlign: 'center',
            backgroundColor: 'rgba(255, 255, 255, 0.9)',
            padding: '20px',
            borderRadius: '8px',
            border: '2px dashed #6c757d'
          }}>
            <h3 style={{ color: '#6c757d', margin: '0 0 10px 0' }}>👁️ Mode Observation</h3>
            <p style={{ color: '#6c757d', margin: 0 }}>
              Vous pouvez voir les modifications mais pas éditer.<br/>
              Demandez l'accès pour modifier le dessin.
            </p>
          </div>
        )}
      </div>

      {/* Instructions */}
      <div style={{ 
        marginTop: '20px', 
        textAlign: 'center',
        padding: '15px',
        backgroundColor: '#e9ecef',
        borderRadius: '4px'
      }}>
        <p style={{ margin: 0, color: '#495057' }}>
          <strong>Instructions:</strong> {hasAccess 
            ? 'Cliquez et glissez pour dessiner sur le canvas' 
            : 'Demandez l\'accès en édition pour pouvoir dessiner'}
        </p>
      </div>

      {/* User Info */}
      <div style={{ 
        marginTop: '15px',
        padding: '10px',
        backgroundColor: '#d1ecf1',
        borderRadius: '4px',
        border: '1px solid #bee5eb'
      }}>
        <p style={{ margin: 0, color: '#0c5460', fontSize: '14px' }}>
          <strong>Utilisateur:</strong> {userName} | 
          <strong> Rôle:</strong> {userRole} | 
          <strong> Projet:</strong> #{projectId}
        </p>
      </div>
    </div>
  );
};

export default SimpleCADViewer;
