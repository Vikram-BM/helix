import React, { useState } from 'react';
import { OutreachStep as OutreachStepType } from '../types';

interface OutreachStepProps {
  step: OutreachStepType;
  onUpdate: (stepId: string, updates: Partial<OutreachStepType>) => void;
}

const OutreachStep: React.FC<OutreachStepProps> = ({ step, onUpdate }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editedContent, setEditedContent] = useState(step.content);
  const [editedSubject, setEditedSubject] = useState(step.subject || '');
  
  const handleSave = () => {
    const updates: Partial<OutreachStepType> = {
      content: editedContent,
    };
    
    if (step.type === 'email') {
      updates.subject = editedSubject;
    }
    
    onUpdate(step.id, updates);
    setIsEditing(false);
  };
  
  const handleCancel = () => {
    setEditedContent(step.content);
    setEditedSubject(step.subject || '');
    setIsEditing(false);
  };
  
  const getStepIcon = () => {
    switch (step.type) {
      case 'email':
        return '✉️';
      case 'linkedin':
        return '🔗';
      case 'phone':
        return '☎️';
      default:
        return '📝';
    }
  };
  
  return (
    <div className={`outreach-step ${step.type}`}>
      <div className="step-header">
        <div className="step-number">
          <span className="step-icon">{getStepIcon()}</span>
          <span>Step {step.stepNumber}</span>
        </div>
        <div className="step-type">{step.type.toUpperCase()}</div>
        <div className="step-timing">
          {step.timing && (
            <span className="timing-info">
              {step.timing}
            </span>
          )}
        </div>
        <div className="step-actions">
          {isEditing ? (
            <>
              <button className="save-btn" onClick={handleSave}>
                Save
              </button>
              <button className="cancel-btn" onClick={handleCancel}>
                Cancel
              </button>
            </>
          ) : (
            <button className="edit-btn" onClick={() => setIsEditing(true)}>
              Edit
            </button>
          )}
        </div>
      </div>
      
      {isEditing ? (
        <div className="step-edit-form">
          {step.type === 'email' && (
            <div className="subject-field">
              <label htmlFor={`subject-${step.id}`}>Subject:</label>
              <input
                id={`subject-${step.id}`}
                type="text"
                value={editedSubject}
                onChange={(e) => setEditedSubject(e.target.value)}
                placeholder="Email subject"
              />
            </div>
          )}
          <textarea
            value={editedContent}
            onChange={(e) => setEditedContent(e.target.value)}
            placeholder="Step content"
            rows={6}
          />
        </div>
      ) : (
        <div className="step-content">
          {step.type === 'email' && step.subject && (
            <div className="step-subject">
              <strong>Subject:</strong> {step.subject}
            </div>
          )}
          <div className="step-message">
            {step.content.split('\n').map((line, i) => (
              <p key={i}>{line}</p>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default OutreachStep;