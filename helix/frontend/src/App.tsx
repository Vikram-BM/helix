import React from 'react';
import ChatPanel from './components/ChatPanel';
import WorkspacePanel from './components/WorkspacePanel';
import { useApp } from './contexts/AppContext';
import './App.css';

const App: React.FC = () => {
  const { 
    messages, 
    sequence, 
    isLoading, 
    sendMessage, 
    updateSequence, 
    updateStep 
  } = useApp();
  
  return (
    <div className="app">
      <header className="app-header">
        <h1>Helix: The Agentic Recruiter</h1>
      </header>
      
      <main className="app-main">
        <div className="panel-container">
          <div className="panel-left">
            <ChatPanel 
              messages={messages} 
              onSendMessage={sendMessage} 
              isLoading={isLoading}
            />
          </div>
          
          <div className="panel-right">
            <WorkspacePanel 
              sequence={sequence} 
              onUpdateStep={updateStep}
              onUpdateSequence={updateSequence}
            />
          </div>
        </div>
      </main>
      
      <footer className="app-footer">
        <p>Helix - Intelligent Outreach Sequences</p>
      </footer>
    </div>
  );
};

export default App;