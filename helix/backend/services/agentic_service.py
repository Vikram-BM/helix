import os
import json
import openai
from datetime import datetime, UTC
import uuid

# This class will have db set from app.py
class AgenticService:
    # Class variable for the db instance - will be set from app.py
    db = None
    
    def __init__(self):
        # Use environment variable for API key with a placeholder as fallback
        api_key = os.getenv('OPENAI_API_KEY', 'your-api-key-here')
        self.client = openai.OpenAI(api_key=api_key)
        self.model = os.getenv('OPENAI_MODEL', 'gpt-4o')
        self.system_message = """
        You are Helix, an AI recruiting assistant specialized in creating outreach sequences for recruiters.
        
        Your goal is to help recruiters create effective, personalized outreach sequences for contacting candidates.
        
        When talking with users:
        1. Be concise, professional, and helpful.
        2. Ask clarifying questions when needed to understand the outreach needs.
        3. Remember information the user has already provided (company, role, etc).
        
        You have access to the following tools:
        
        generate_sequence: Generate a complete outreach sequence based on gathered information.
        Parameters:
        - company_name: The name of the company recruiting
        - role_name: The position being recruited for
        - candidate_persona: Description of the ideal candidate
        
        update_sequence: Update an existing outreach sequence.
        Parameters:
        - sequence_id: The ID of the sequence to update
        - updates: A dictionary of updates to apply
        
        add_sequence_step: Add a new step to an outreach sequence.
        Parameters:
        - sequence_id: The ID of the sequence to update
        - step_type: The type of outreach (email, linkedin, phone, other)
        - content: The message content
        - subject: Email subject (for email type only)
        - timing: When this step should occur (e.g., "Day 3")
        
        update_sequence_step: Update an existing step in a sequence.
        Parameters:
        - step_id: The ID of the step to update
        - updates: A dictionary of updates to apply
        
        IMPORTANT: Once you've collected enough information to generate an outreach sequence (company, role, candidate persona), use the generate_sequence tool to create it. Don't ask unnecessary questions once you have the essential information.
        """
    
    def process_message(self, user_message, session):
        messages = [{"role": "system", "content": self.system_message}]
        
        # Add conversation history
        for msg in session.messages:
            messages.append({"role": msg.role, "content": msg.content})
        
        # Add user's new message
        messages.append({"role": "user", "content": user_message.content})
        
        # Function definitions
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "generate_sequence",
                    "description": "Generate a complete outreach sequence based on gathered information",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "company_name": {
                                "type": "string",
                                "description": "The name of the company recruiting"
                            },
                            "role_name": {
                                "type": "string",
                                "description": "The position being recruited for"
                            },
                            "candidate_persona": {
                                "type": "string",
                                "description": "Description of the ideal candidate"
                            }
                        },
                        "required": ["company_name", "role_name", "candidate_persona"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_sequence",
                    "description": "Update an existing outreach sequence",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "sequence_id": {
                                "type": "string",
                                "description": "The ID of the sequence to update"
                            },
                            "updates": {
                                "type": "object",
                                "description": "A dictionary of updates to apply",
                                "properties": {
                                    "name": {"type": "string"},
                                    "company_name": {"type": "string"},
                                    "role_name": {"type": "string"},
                                    "candidate_persona": {"type": "string"}
                                }
                            }
                        },
                        "required": ["sequence_id", "updates"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "add_sequence_step",
                    "description": "Add a new step to an outreach sequence",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "sequence_id": {
                                "type": "string",
                                "description": "The ID of the sequence to update"
                            },
                            "step_type": {
                                "type": "string",
                                "enum": ["email", "linkedin", "phone", "other"],
                                "description": "The type of outreach"
                            },
                            "content": {
                                "type": "string",
                                "description": "The message content"
                            },
                            "subject": {
                                "type": "string",
                                "description": "Email subject (for email type only)"
                            },
                            "timing": {
                                "type": "string",
                                "description": "When this step should occur (e.g., 'Day 3')"
                            },
                            "wait_time": {
                                "type": "integer",
                                "description": "Number of days to wait after previous step"
                            }
                        },
                        "required": ["sequence_id", "step_type", "content"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_sequence_step",
                    "description": "Update an existing step in a sequence",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "step_id": {
                                "type": "string",
                                "description": "The ID of the step to update"
                            },
                            "updates": {
                                "type": "object",
                                "description": "A dictionary of updates to apply",
                                "properties": {
                                    "content": {"type": "string"},
                                    "subject": {"type": "string"},
                                    "type": {"type": "string", "enum": ["email", "linkedin", "phone", "other"]},
                                    "timing": {"type": "string"},
                                    "wait_time": {"type": "integer"}
                                }
                            }
                        },
                        "required": ["step_id", "updates"]
                    }
                }
            }
        ]
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=tools,
                tool_choice="auto"
            )
            
            assistant_message = response.choices[0].message
            
            # Check if the assistant wants to call a function
            if assistant_message.tool_calls:
                tool_call = assistant_message.tool_calls[0]
                
                # Create a tool call notification message
                from app import Message
                
                tool_call_message = Message(
                    id=str(uuid.uuid4()),
                    session_id=session.id,
                    role="assistant",
                    content=assistant_message.content or "I'll help with that.",
                    tool_call=json.dumps({
                        "name": tool_call.function.name,
                        "status": "calling"
                    }),
                    created_at=datetime.now(UTC)
                )
                
                self.db.session.add(tool_call_message)
                self.db.session.commit()
                
                # Process the tool call
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                result = self.execute_function(function_name, function_args, session)
                
                # Update the tool call message with the result
                tool_call_message.tool_call = json.dumps({
                    "name": tool_call.function.name,
                    "status": "completed",
                    "result": result
                })
                
                self.db.session.commit()
                
                # Get the AI's response to the function result
                messages.append({
                    "role": "assistant",
                    "content": assistant_message.content,
                    "tool_calls": [
                        {
                            "id": tool_call.id,
                            "type": "function",
                            "function": {
                                "name": tool_call.function.name,
                                "arguments": tool_call.function.arguments
                            }
                        }
                    ]
                })
                
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })
                
                second_response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages
                )
                
                from app import Message
                
                final_message = Message(
                    id=str(uuid.uuid4()),
                    session_id=session.id,
                    role="assistant",
                    content=second_response.choices[0].message.content,
                    created_at=datetime.now(UTC)
                )
                
                self.db.session.add(final_message)
                self.db.session.commit()
                
                return final_message
            else:
                # No function call, just a regular message
                from app import Message
                
                assistant_response = Message(
                    id=str(uuid.uuid4()),
                    session_id=session.id,
                    role="assistant",
                    content=assistant_message.content,
                    created_at=datetime.now(UTC)
                )
                
                self.db.session.add(assistant_response)
                self.db.session.commit()
                
                return assistant_response
        
        except Exception as e:
            print(f"Error processing message: {e}")
            
            from app import Message
            
            error_message = Message(
                id=str(uuid.uuid4()),
                session_id=session.id,
                role="assistant",
                content="I apologize, but I encountered an error processing your request. Please try again.",
                created_at=datetime.now(UTC)
            )
            
            self.db.session.add(error_message)
            self.db.session.commit()
            
            return error_message
    
    def execute_function(self, function_name, args, session):
        try:
            if function_name == "generate_sequence":
                return self.generate_sequence(
                    args.get("company_name"),
                    args.get("role_name"),
                    args.get("candidate_persona"),
                    session
                )
            elif function_name == "update_sequence":
                return self.update_sequence(
                    args.get("sequence_id"),
                    args.get("updates")
                )
            elif function_name == "add_sequence_step":
                return self.add_sequence_step(
                    args.get("sequence_id"),
                    args.get("step_type"),
                    args.get("content"),
                    args.get("subject"),
                    args.get("timing"),
                    args.get("wait_time")
                )
            elif function_name == "update_sequence_step":
                return self.update_sequence_step(
                    args.get("step_id"),
                    args.get("updates")
                )
            else:
                return f"Unknown function: {function_name}"
        except Exception as e:
            return f"Error executing function {function_name}: {str(e)}"
    
    def generate_sequence(self, company_name, role_name, candidate_persona, session):
        try:
            # Create a new sequence
            # Reference model from app
            from app import OutreachSequence
            
            sequence = OutreachSequence(
                id=str(uuid.uuid4()),
                user_id=session.user_id,
                name=f"{role_name} at {company_name} Outreach",
                company_name=company_name,
                role_name=role_name,
                candidate_persona=candidate_persona,
                created_at=datetime.now(UTC),
                updated_at=datetime.now(UTC)
            )
            
            self.db.session.add(sequence)
            
            # Update the session with the current sequence
            session.current_sequence_id = sequence.id
            
            self.db.session.commit()
            
            # Generate steps using LLM
            steps_prompt = f"""
            Create a 3-5 step outreach sequence for recruiting a {role_name} candidate for {company_name}.
            The ideal candidate persona is: {candidate_persona}
            
            For each step, provide:
            1. Type (email, linkedin, phone)
            2. Timing (which day)
            3. Subject (for emails)
            4. Message content
            
            Make the sequence professional but personable. Focus on what would appeal to this specific candidate persona.
            """
            
            steps_response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a recruiting outreach expert. Create effective, professional outreach sequences."},
                    {"role": "user", "content": steps_prompt}
                ]
            )
            
            steps_text = steps_response.choices[0].message.content
            
            # Parse the generated steps and create them
            # Note: In a real implementation, this would be more robust
            # This is a simplified parsing method
            current_step = None
            step_number = 1
            step_type = None
            subject = None
            timing = None
            content_lines = []
            
            for line in steps_text.split('\n'):
                line = line.strip()
                
                if not line:
                    continue
                
                # Check for a new step indicator
                if line.startswith("Step") or line.startswith("#") or line.lower().startswith("day"):
                    # Save the previous step if it exists
                    if current_step and step_type and content_lines:
                        from app import OutreachStep
                        
                        step = OutreachStep(
                            id=str(uuid.uuid4()),
                            sequence_id=sequence.id,
                            step_number=step_number,
                            type=step_type.lower(),
                            content='\n'.join(content_lines),
                            subject=subject,
                            timing=timing,
                            wait_time=step_number - 1,
                            created_at=datetime.now(UTC),
                            updated_at=datetime.now(UTC)
                        )
                        
                        self.db.session.add(step)
                        step_number += 1
                    
                    # Start a new step
                    current_step = line
                    step_type = None
                    subject = None
                    timing = None
                    content_lines = []
                
                # Try to identify step properties
                elif "type:" in line.lower() or "channel:" in line.lower():
                    if "email" in line.lower():
                        step_type = "email"
                    elif "linkedin" in line.lower():
                        step_type = "linkedin"
                    elif "phone" in line.lower() or "call" in line.lower():
                        step_type = "phone"
                    else:
                        step_type = "other"
                
                elif "subject:" in line.lower() and "email" in step_type:
                    subject = line.split(":", 1)[1].strip()
                
                elif "timing:" in line.lower() or "day:" in line.lower():
                    timing = line.split(":", 1)[1].strip()
                
                # If we've already identified a step type, consider the rest as content
                elif step_type and not line.startswith('-') and not line.startswith('*'):
                    content_lines.append(line)
            
            # Don't forget to add the last step
            if current_step and step_type and content_lines:
                from app import OutreachStep
                
                step = OutreachStep(
                    id=str(uuid.uuid4()),
                    sequence_id=sequence.id,
                    step_number=step_number,
                    type=step_type.lower(),
                    content='\n'.join(content_lines),
                    subject=subject,
                    timing=timing,
                    wait_time=step_number - 1,
                    created_at=datetime.now(UTC),
                    updated_at=datetime.now(UTC)
                )
                
                self.db.session.add(step)
            
            self.db.session.commit()
            
            # Return a success message
            return f"Created outreach sequence '{sequence.name}' with {step_number} steps"
        
        except Exception as e:
            self.db.session.rollback()
            return f"Error generating sequence: {str(e)}"
    
    def update_sequence(self, sequence_id, updates):
        try:
            from app import OutreachSequence
            sequence = self.db.session.get(OutreachSequence, sequence_id)
            
            if not sequence:
                return f"Sequence with ID {sequence_id} not found"
            
            if "name" in updates:
                sequence.name = updates["name"]
            
            if "company_name" in updates:
                sequence.company_name = updates["company_name"]
            
            if "role_name" in updates:
                sequence.role_name = updates["role_name"]
            
            if "candidate_persona" in updates:
                sequence.candidate_persona = updates["candidate_persona"]
            
            sequence.updated_at = datetime.utcnow()
            self.db.session.commit()
            
            return f"Updated sequence '{sequence.name}' successfully"
        
        except Exception as e:
            self.db.session.rollback()
            return f"Error updating sequence: {str(e)}"
    
    def add_sequence_step(self, sequence_id, step_type, content, subject=None, timing=None, wait_time=None):
        try:
            from app import OutreachSequence
            sequence = self.db.session.get(OutreachSequence, sequence_id)
            
            if not sequence:
                return f"Sequence with ID {sequence_id} not found"
            
            # Determine the next step number
            next_step_number = 1
            if sequence.steps:
                next_step_number = max(step.step_number for step in sequence.steps) + 1
            
            from app import OutreachStep
            step = OutreachStep(
                id=str(uuid.uuid4()),
                sequence_id=sequence_id,
                step_number=next_step_number,
                type=step_type,
                content=content,
                subject=subject,
                timing=timing,
                wait_time=wait_time or (next_step_number - 1),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            self.db.session.add(step)
            self.db.session.commit()
            
            return f"Added {step_type} step to sequence '{sequence.name}'"
        
        except Exception as e:
            self.db.session.rollback()
            return f"Error adding sequence step: {str(e)}"
    
    def update_sequence_step(self, step_id, updates):
        try:
            from app import OutreachStep
            step = self.db.session.get(OutreachStep, step_id)
            
            if not step:
                return f"Step with ID {step_id} not found"
            
            if "content" in updates:
                step.content = updates["content"]
            
            if "subject" in updates:
                step.subject = updates["subject"]
            
            if "type" in updates:
                step.type = updates["type"]
            
            if "timing" in updates:
                step.timing = updates["timing"]
            
            if "wait_time" in updates:
                step.wait_time = updates["wait_time"]
            
            step.updated_at = datetime.utcnow()
            self.db.session.commit()
            
            return f"Updated step {step.step_number} successfully"
        
        except Exception as e:
            self.db.session.rollback()
            return f"Error updating sequence step: {str(e)}"