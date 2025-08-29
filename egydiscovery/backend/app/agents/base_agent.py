"""
Base Agent Interface for Egypt Tourism SaaS Platform
Provides common functionality for all specialized agents
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from datetime import datetime
import uuid
import asyncio
from loguru import logger
from pydantic import BaseModel, Field
import json

class AgentMessage(BaseModel):
    """Standard message format for agent communication"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    sender: str
    recipient: str
    message_type: str
    content: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.now)
    priority: int = Field(default=1, ge=1, le=10)
    requires_response: bool = False

class AgentResponse(BaseModel):
    """Standard response format for agent operations"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)
    execution_time: Optional[float] = None

class BaseAgent(ABC):
    """Abstract base class for all agents in the system"""

    def __init__(self, agent_id: str, name: str, config: Dict[str, Any]):
        self.agent_id = agent_id
        self.name = name
        self.config = config
        self.status = "initialized"
        self.created_at = datetime.now()
        self.message_queue: List[AgentMessage] = []
        self.knowledge_base = {}
        self.metrics = {
            "messages_processed": 0,
            "successful_operations": 0,
            "failed_operations": 0,
            "average_response_time": 0.0
        }

        # Initialize logging
        logger.add(f"logs/{self.agent_id}.log", rotation="1 day")
        logger.info(f"Agent {self.name} initialized with ID: {self.agent_id}")

    @abstractmethod
    async def process_message(self, message: AgentMessage) -> AgentResponse:
        """Process incoming messages from other agents or the master controller"""
        pass

    @abstractmethod
    async def execute_task(self, task: Dict[str, Any]) -> AgentResponse:
        """Execute a specific task assigned by the master controller"""
        pass

    @abstractmethod
    async def get_capabilities(self) -> List[str]:
        """Return list of capabilities this agent provides"""
        pass

    async def start(self):
        """Start the agent and begin processing messages"""
        self.status = "running"
        logger.info(f"Agent {self.name} started")
        await self._message_processing_loop()

    async def stop(self):
        """Stop the agent gracefully"""
        self.status = "stopped"
        logger.info(f"Agent {self.name} stopped")

    async def send_message(self, message: AgentMessage):
        """Send message to another agent or master controller"""
        logger.info(f"Sending message from {self.name} to {message.recipient}")
        # In a real implementation, this would use a message broker
        # For now, we'll simulate the message sending
        return True

    async def _message_processing_loop(self):
        """Internal message processing loop"""
        while self.status == "running":
            if self.message_queue:
                message = self.message_queue.pop(0)
                try:
                    start_time = datetime.now()
                    response = await self.process_message(message)
                    execution_time = (datetime.now() - start_time).total_seconds()

                    # Update metrics
                    self.metrics["messages_processed"] += 1
                    if response.success:
                        self.metrics["successful_operations"] += 1
                    else:
                        self.metrics["failed_operations"] += 1

                    # Update average response time
                    total_ops = self.metrics["successful_operations"] + self.metrics["failed_operations"]
                    current_avg = self.metrics["average_response_time"]
                    self.metrics["average_response_time"] = (
                        (current_avg * (total_ops - 1) + execution_time) / total_ops
                    )

                    logger.info(f"Message processed by {self.name} in {execution_time:.2f}s")

                except Exception as e:
                    logger.error(f"Error processing message in {self.name}: {str(e)}")
                    self.metrics["failed_operations"] += 1

            await asyncio.sleep(0.1)  # Small delay to prevent busy waiting

    def add_message_to_queue(self, message: AgentMessage):
        """Add message to processing queue"""
        self.message_queue.append(message)
        logger.info(f"Message queued for {self.name}")

    def get_status(self) -> Dict[str, Any]:
        """Get current agent status and metrics"""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "queue_length": len(self.message_queue),
            "metrics": self.metrics
        }

    def update_knowledge_base(self, key: str, value: Any):
        """Update agent's knowledge base"""
        self.knowledge_base[key] = value
        logger.info(f"Knowledge base updated for {self.name}: {key}")

    def get_knowledge(self, key: str) -> Any:
        """Retrieve knowledge from agent's knowledge base"""
        return self.knowledge_base.get(key)
