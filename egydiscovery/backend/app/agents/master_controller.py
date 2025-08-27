"""
Master Agent Controller for Egypt Tourism SaaS Platform
Manages all specialized agents and coordinates system operations
"""

import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime
from loguru import logger
from pydantic import BaseModel
import json
import uuid

from agents.base.base_agent import BaseAgent, AgentMessage, AgentResponse

class PromptTemplate(BaseModel):
    """Template for prompt-based agent management"""
    name: str
    description: str
    template: str
    parameters: List[str]
    agent_type: str

class SystemCommand(BaseModel):
    """Command structure for system operations"""
    command_id: str
    command_type: str
    target_agent: Optional[str] = None
    parameters: Dict[str, Any]
    priority: int = 1
    created_at: datetime
    executed_at: Optional[datetime] = None
    status: str = "pending"

class MasterAgentController:
    """
    Master controller that manages all agents in the Egypt Tourism SaaS system.
    Provides prompt-based management and coordination of agent operations.
    """

    def __init__(self, config: Dict[str, Any]):
        self.controller_id = str(uuid.uuid4())
        self.config = config
        self.agents: Dict[str, BaseAgent] = {}
        self.command_queue: List[SystemCommand] = []
        self.prompt_templates: Dict[str, PromptTemplate] = {}
        self.system_status = "initialized"
        self.created_at = datetime.now()

        # Initialize logging
        logger.add("logs/master_controller.log", rotation="1 day")
        logger.info(f"Master Agent Controller initialized: {self.controller_id}")

        # Load default prompt templates
        self._initialize_prompt_templates()

    def _initialize_prompt_templates(self):
        """Initialize default prompt templates for agent management"""
        templates = [
            {
                "name": "customer_service_response",
                "description": "Generate customer service response in Arabic/English",
                "template": """
                You are a professional customer service agent for Egypt Tourism SaaS.
                Customer Query: {customer_query}
                Language: {language}
                Context: {context}

                Generate a helpful, accurate response that:
                - Addresses the customer's specific question
                - Provides relevant Egypt tourism information
                - Maintains professional tone
                - Uses the specified language ({language})
                """,
                "parameters": ["customer_query", "language", "context"],
                "agent_type": "customer_service"
            },
            {
                "name": "trip_planning",
                "description": "Create personalized trip plan for Egypt",
                "template": """
                Create a detailed trip plan for Egypt tourism.

                Customer Profile:
                - Budget: {budget}
                - Duration: {duration} days
                - Interests: {interests}
                - Travel Style: {travel_style}
                - Group Size: {group_size}

                Requirements:
                - Include popular Egypt destinations (Pyramids, Luxor, Aswan, Red Sea)
                - Provide day-by-day itinerary
                - Include accommodation recommendations
                - Suggest transportation options
                - Estimate total costs
                - Consider seasonal factors
                """,
                "parameters": ["budget", "duration", "interests", "travel_style", "group_size"],
                "agent_type": "trip_planner"
            },
            {
                "name": "marketing_campaign",
                "description": "Create marketing campaign for Egypt tourism",
                "template": """
                Design a marketing campaign for Egypt tourism.

                Campaign Parameters:
                - Target Audience: {target_audience}
                - Budget: {campaign_budget}
                - Duration: {campaign_duration}
                - Platforms: {platforms}
                - Goals: {goals}

                Create:
                - Campaign strategy
                - Ad copy variations
                - Targeting parameters
                - Budget allocation
                - Success metrics
                - Timeline
                """,
                "parameters": ["target_audience", "campaign_budget", "campaign_duration", "platforms", "goals"],
                "agent_type": "marketing"
            },
            {
                "name": "data_analysis",
                "description": "Analyze tourism data and generate insights",
                "template": """
                Analyze the provided tourism data and generate actionable insights.

                Data Context:
                - Data Type: {data_type}
                - Time Period: {time_period}
                - Metrics: {metrics}
                - Focus Areas: {focus_areas}

                Provide:
                - Key trends and patterns
                - Performance indicators
                - Anomalies or issues
                - Recommendations
                - Visualizations suggestions
                """,
                "parameters": ["data_type", "time_period", "metrics", "focus_areas"],
                "agent_type": "data_analysis"
            }
        ]

        for template_data in templates:
            template = PromptTemplate(**template_data)
            self.prompt_templates[template.name] = template

    async def register_agent(self, agent: BaseAgent):
        """Register a specialized agent with the master controller"""
        self.agents[agent.agent_id] = agent
        logger.info(f"Agent registered: {agent.name} ({agent.agent_id})")

        # Send welcome message to agent
        welcome_message = AgentMessage(
            sender="master_controller",
            recipient=agent.agent_id,
            message_type="system_welcome",
            content={
                "message": "Welcome to Egypt Tourism SaaS System",
                "controller_id": self.controller_id,
                "system_status": self.system_status
            }
        )
        agent.add_message_to_queue(welcome_message)

    async def unregister_agent(self, agent_id: str):
        """Unregister an agent from the system"""
        if agent_id in self.agents:
            agent = self.agents[agent_id]
            await agent.stop()
            del self.agents[agent_id]
            logger.info(f"Agent unregistered: {agent_id}")

    async def execute_prompt_command(self, prompt_name: str, parameters: Dict[str, Any]) -> AgentResponse:
        """Execute a prompt-based command"""
        if prompt_name not in self.prompt_templates:
            return AgentResponse(
                success=False,
                error=f"Prompt template '{prompt_name}' not found"
            )

        template = self.prompt_templates[prompt_name]

        # Find appropriate agent for this prompt type
        target_agent = None
        for agent in self.agents.values():
            capabilities = await agent.get_capabilities()
            if template.agent_type in capabilities:
                target_agent = agent
                break

        if not target_agent:
            return AgentResponse(
                success=False,
                error=f"No agent available for type '{template.agent_type}'"
            )

        # Format prompt with parameters
        try:
            formatted_prompt = template.template.format(**parameters)
        except KeyError as e:
            return AgentResponse(
                success=False,
                error=f"Missing required parameter: {e}"
            )

        # Create task for target agent
        task = {
            "type": "prompt_execution",
            "prompt": formatted_prompt,
            "template_name": prompt_name,
            "parameters": parameters
        }

        # Execute task
        start_time = datetime.now()
        response = await target_agent.execute_task(task)
        execution_time = (datetime.now() - start_time).total_seconds()
        response.execution_time = execution_time

        logger.info(f"Prompt command '{prompt_name}' executed in {execution_time:.2f}s")
        return response

    async def process_natural_language_command(self, command: str, context: Dict[str, Any] = None) -> AgentResponse:
        """Process natural language commands and route to appropriate agents"""
        context = context or {}

        # Simple command routing based on keywords
        command_lower = command.lower()

        if any(word in command_lower for word in ["customer", "support", "help", "question"]):
            return await self.execute_prompt_command("customer_service_response", {
                "customer_query": command,
                "language": context.get("language", "english"),
                "context": json.dumps(context)
            })

        elif any(word in command_lower for word in ["trip", "plan", "itinerary", "travel"]):
            return await self.execute_prompt_command("trip_planning", {
                "budget": context.get("budget", "moderate"),
                "duration": context.get("duration", "7"),
                "interests": context.get("interests", "historical sites, culture"),
                "travel_style": context.get("travel_style", "comfortable"),
                "group_size": context.get("group_size", "2")
            })

        elif any(word in command_lower for word in ["marketing", "campaign", "ads", "promote"]):
            return await self.execute_prompt_command("marketing_campaign", {
                "target_audience": context.get("target_audience", "international tourists"),
                "campaign_budget": context.get("campaign_budget", "$10000"),
                "campaign_duration": context.get("campaign_duration", "30 days"),
                "platforms": context.get("platforms", "Facebook, Google Ads"),
                "goals": context.get("goals", "increase bookings")
            })

        elif any(word in command_lower for word in ["analyze", "data", "report", "insights"]):
            return await self.execute_prompt_command("data_analysis", {
                "data_type": context.get("data_type", "booking data"),
                "time_period": context.get("time_period", "last 30 days"),
                "metrics": context.get("metrics", "revenue, bookings, conversion"),
                "focus_areas": context.get("focus_areas", "performance optimization")
            })

        else:
            return AgentResponse(
                success=False,
                error="Unable to understand command. Please provide more specific instructions."
            )

    async def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        agent_statuses = {}
        for agent_id, agent in self.agents.items():
            agent_statuses[agent_id] = agent.get_status()

        return {
            "controller_id": self.controller_id,
            "system_status": self.system_status,
            "created_at": self.created_at.isoformat(),
            "total_agents": len(self.agents),
            "active_agents": len([a for a in self.agents.values() if a.status == "running"]),
            "command_queue_length": len(self.command_queue),
            "available_prompts": list(self.prompt_templates.keys()),
            "agents": agent_statuses
        }

    async def start_system(self):
        """Start the entire system and all registered agents"""
        self.system_status = "running"
        logger.info("Starting Egypt Tourism SaaS system...")

        # Start all registered agents
        start_tasks = []
        for agent in self.agents.values():
            start_tasks.append(agent.start())

        if start_tasks:
            await asyncio.gather(*start_tasks, return_exceptions=True)

        logger.info("Egypt Tourism SaaS system started successfully")

    async def stop_system(self):
        """Stop the entire system gracefully"""
        self.system_status = "stopping"
        logger.info("Stopping Egypt Tourism SaaS system...")

        # Stop all agents
        stop_tasks = []
        for agent in self.agents.values():
            stop_tasks.append(agent.stop())

        if stop_tasks:
            await asyncio.gather(*stop_tasks, return_exceptions=True)

        self.system_status = "stopped"
        logger.info("Egypt Tourism SaaS system stopped")

    def add_custom_prompt_template(self, template: PromptTemplate):
        """Add a custom prompt template"""
        self.prompt_templates[template.name] = template
        logger.info(f"Custom prompt template added: {template.name}")

    async def broadcast_message(self, message_type: str, content: Dict[str, Any]):
        """Broadcast message to all agents"""
        for agent in self.agents.values():
            message = AgentMessage(
                sender="master_controller",
                recipient=agent.agent_id,
                message_type=message_type,
                content=content
            )
            agent.add_message_to_queue(message)

        logger.info(f"Broadcast message sent to {len(self.agents)} agents")
