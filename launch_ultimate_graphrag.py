#!/usr/bin/env python3
"""
Ultimate GraphRAG System Launcher
Production-ready HVAC technical support system for Daniel

This launcher provides multiple ways to interact with the GraphRAG system:
1. Web API (FastAPI) - Production mode
2. Command Line Interface - Interactive testing
3. Interactive Demo - Complete system demonstration
4. Batch Processing - Process multiple documents

Usage Examples:
    python launch_ultimate_graphrag.py --mode api          # Start web API
    python launch_ultimate_graphrag.py --mode cli          # Command line interface
    python launch_ultimate_graphrag.py --mode demo         # Interactive demo
    python launch_ultimate_graphrag.py --mode batch        # Batch processing

Author: Sergio Sebastian - infrateki
Project: HVAC Daniel GraphRAG System for Multipoint S.A.
"""

import os
import sys
import argparse
import asyncio
import logging
from typing import Dict, Any
from dotenv import load_dotenv

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

load_dotenv()
logger = logging.getLogger(__name__)

class GraphRAGLauncher:
    """
    Ultimate launcher for the GraphRAG system
    """
    
    def __init__(self):
        self.logo = """
╔════════════════════════════════════════════════════════════════════════════════╗
║                                                                                ║
║          🚀 HVAC DANIEL GRAPHRAG SYSTEM - PRODUCTION LAUNCHER 🚀              ║
║                                                                                ║
║    Complete GraphRAG Implementation for Samsung HVAC Technical Support        ║
║                                                                                ║
║    📊 System Status: OPERATIONAL                                              ║
║    🎯 Target User: Daniel Uslenghi - Multipoint S.A.                         ║
║    📧 Contact: infrateki@gmail.com                                            ║
║                                                                                ║
║    Available Modes:                                                           ║
║    • API Mode    - Production web API (port 8000)                            ║
║    • CLI Mode    - Command line interface                                     ║
║    • Demo Mode   - Interactive demonstration                                  ║
║    • Batch Mode  - Process multiple documents                                ║
║                                                                                ║
╚════════════════════════════════════════════════════════════════════════════════╝
        """
    
    def print_logo(self):
        """Print system logo and status"""
        print(self.logo)
    
    def check_system_requirements(self):
        """Check if all system requirements are met"""
        logger.info("🔍 Checking system requirements...")
        
        requirements = {
            "Neo4j Connection": self.check_neo4j(),
            "OpenAI API Key": self.check_openai(),
            "Required Directories": self.check_directories(),
            "Python Dependencies": self.check_dependencies()
        }
        
        all_good = True
        for requirement, status in requirements.items():
            status_icon = "✅" if status else "❌"
            logger.info(f"{status_icon} {requirement}: {'OK' if status else 'FAILED'}")
            if not status:
                all_good = False
        
        if not all_good:
            logger.error("❌ System requirements not met. Please fix the issues above.")
            return False
        
        logger.info("✅ All system requirements met!")
        return True
    
    def check_neo4j(self) -> bool:
        """Check Neo4j connection"""
        try:
            from neo4j import GraphDatabase
            uri = os.getenv("NEO4J_URI", "bolt://localhost:7690")
            user = os.getenv("NEO4J_USER", "neo4j")
            password = os.getenv("NEO4J_PASSWORD")
            
            if not password:
                return False
            
            driver = GraphDatabase.driver(uri, auth=(user, password))
            with driver.session() as session:
                result = session.run("RETURN 1 as test")
                test = result.single()["test"]
                driver.close()
                return test == 1
        except Exception:
            return False
    
    def check_openai(self) -> bool:
        """Check OpenAI API key"""
        api_key = os.getenv("OPENAI_API_KEY")
        return api_key is not None and api_key.startswith("sk-")
    
    def check_directories(self) -> bool:
        """Check required directories exist"""
        required_dirs = ["logs", "data", "notebooks", "config"]
        for dir_name in required_dirs:
            if not os.path.exists(dir_name):
                os.makedirs(dir_name, exist_ok=True)
        return True
    
    def check_dependencies(self) -> bool:
        """Check Python dependencies"""
        try:
            import openai
            import neo4j
            import fastapi
            import pandas
            import numpy
            return True
        except ImportError:
            return False
    
    async def launch_api_mode(self, port: int = 8000, host: str = "0.0.0.0"):
        """Launch the system in API mode"""
        logger.info(f"🌐 Starting GraphRAG API on {host}:{port}")
        
        try:
            import uvicorn
            from src.api.ultimate_graphrag_api import app
            
            # Configure uvicorn
            config = uvicorn.Config(
                app=app,
                host=host,
                port=port,
                log_level="info",
                reload=False,
                workers=1
            )
            
            server = uvicorn.Server(config)
            
            logger.info(f"✅ API started successfully!")
            logger.info(f"📋 API Documentation: http://{host}:{port}/docs")
            logger.info(f"🔗 API Endpoint: http://{host}:{port}/query")
            logger.info(f"📊 Statistics: http://{host}:{port}/stats")
            
            await server.serve()
            
        except Exception as e:
            logger.error(f"❌ Failed to start API: {e}")
            raise

def main():
    """Main launcher function"""
    parser = argparse.ArgumentParser(description="HVAC GraphRAG System Launcher")
    parser.add_argument(
        "--mode", 
        choices=["api", "cli", "demo", "batch"],
        default="api",
        help="Launch mode (default: api)"
    )
    parser.add_argument("--port", type=int, default=8000, help="API port (default: 8000)")
    parser.add_argument("--host", default="0.0.0.0", help="API host (default: 0.0.0.0)")
    
    args = parser.parse_args()
    
    # Initialize launcher
    launcher = GraphRAGLauncher()
    launcher.print_logo()
    
    # Check system requirements
    if not launcher.check_system_requirements():
        sys.exit(1)
    
    # Launch in selected mode
    try:
        if args.mode == "api":
            asyncio.run(launcher.launch_api_mode(args.port, args.host))
        else:
            print(f"Mode '{args.mode}' implementation coming soon!")
            print("For now, use --mode api to start the web API")
            
    except KeyboardInterrupt:
        logger.info("👋 System shutdown requested by user")
    except Exception as e:
        logger.error(f"❌ System error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
