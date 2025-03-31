import React from 'react';
import OutreachStep from './OutreachStep';
import { OutreachSequence, OutreachStep as OutreachStepType } from '../types';

interface WorkspacePanelProps {
  sequence: OutreachSequence | null;
  onUpdateStep: (stepId: string, updates: Partial<OutreachStepType>) => void;
  onUpdateSequence: (updates: Partial<OutreachSequence>) => void;
}

const WorkspacePanel: React.FC<WorkspacePanelProps> = ({
  sequence,
  onUpdateStep,
  onUpdateSequence,
}) => {
  if (!sequence) {
    return (
      <div className="workspace-panel empty-workspace">
        <div className="workspace-header">
          <h2>Outreach Sequence Workspace</h2>
        </div>
        <div className="empty-sequence-message">
          <p>
            Start by describing your needs to Helix to generate an outreach sequence.
          </p>
          <ul>
            <li>What role are you recruiting for?</li>
            <li>What is the target company?</li>
            <li>What is the candidate persona?</li>
          </ul>
        </div>
      </div>
    );
  }

  const handleNameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    onUpdateSequence({ name: e.target.value });
  };

  return (
    <div className="workspace-panel">
      <div className="workspace-header">
        <div className="sequence-name-container">
          <h2>
            <input
              type="text"
              value={sequence.name}
              onChange={handleNameChange}
              placeholder="Sequence Name"
              className="sequence-name-input"
            />
          </h2>
        </div>
        <div className="sequence-meta">
          <div className="sequence-meta-item">
            <span className="meta-label">Company:</span>
            <span className="meta-value">{sequence.companyName}</span>
          </div>
          <div className="sequence-meta-item">
            <span className="meta-label">Role:</span>
            <span className="meta-value">{sequence.roleName}</span>
          </div>
          <div className="sequence-meta-item">
            <span className="meta-label">Candidate:</span>
            <span className="meta-value">{sequence.candidatePersona}</span>
          </div>
        </div>
      </div>

      <div className="sequence-steps">
        {sequence.steps.length > 0 ? (
          sequence.steps
            .sort((a, b) => a.stepNumber - b.stepNumber)
            .map((step) => (
              <OutreachStep
                key={step.id}
                step={step}
                onUpdate={onUpdateStep}
              />
            ))
        ) : (
          <div className="no-steps-message">
            <p>No steps in this sequence yet. Continue chatting with Helix to build your sequence.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default WorkspacePanel;