#!/usr/bin/env python3
"""
Investigation Intelligence System - Main Orchestrator

This is the main entry point for the Investigation Intelligence System.
It coordinates all components: ingestion, processing, analysis, and reporting.
"""

import os
import sys
import yaml
import click
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from loguru import logger

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.logger import setup_logger
from src.ingestion.google_drive import GoogleDriveIngestion
from src.ingestion.dropbox import DropboxIngestion
from src.ingestion.local_folder import LocalFolderIngestion
from src.processing.router import FileRouter
from src.normalization.normalizer import DataNormalizer
from src.analysis.extraction_layer import ExtractionLayer
from src.analysis.context_layer import ContextLayer
from src.analysis.investigation_layer import InvestigationLayer
from src.intelligence.mind_map import MindMapBuilder
from src.intelligence.self_prompting import SelfPromptingEngine
from src.output.pdf_generator import PDFReportGenerator
from src.output.json_exporter import JSONExporter
from src.output.graph_exporter import GraphExporter


class InvestigationSystem:
    """
    Main orchestrator for the Investigation Intelligence System.
    
    This class coordinates all system components and manages the
    investigation workflow from ingestion to report generation.
    """
    
    def __init__(self, config_path: str = "config/config.yaml"):
        """Initialize the investigation system."""
        self.config = self._load_config(config_path)
        self.logger = setup_logger(
            log_level=self.config["system"]["log_level"],
            log_file=self.config["system"]["log_file"]
        )
        
        # Initialize components
        self._init_components()
        
        self.logger.info("Investigation Intelligence System initialized")
    
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file."""
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        # Substitute environment variables
        return self._substitute_env_vars(config)
    
    def _substitute_env_vars(self, config: Any) -> Any:
        """Recursively substitute environment variables in config."""
        if isinstance(config, dict):
            return {k: self._substitute_env_vars(v) for k, v in config.items()}
        elif isinstance(config, list):
            return [self._substitute_env_vars(item) for item in config]
        elif isinstance(config, str) and config.startswith("${") and config.endswith("}"):
            env_var = config[2:-1]
            return os.getenv(env_var, config)
        return config
    
    def _init_components(self):
        """Initialize all system components."""
        # Ingestion components
        if self.config["ingestion"]["google_drive"]["enabled"]:
            self.google_drive = GoogleDriveIngestion(self.config)
        if self.config["ingestion"]["dropbox"]["enabled"]:
            self.dropbox = DropboxIngestion(self.config)
        self.local = LocalFolderIngestion(self.config)
        
        # Processing components
        self.router = FileRouter(self.config)
        self.normalizer = DataNormalizer(self.config)
        
        # Analysis layers
        self.extraction_layer = ExtractionLayer(self.config)
        self.context_layer = ContextLayer(self.config)
        self.investigation_layer = InvestigationLayer(self.config)
        
        # Intelligence components
        self.mind_map_builder = MindMapBuilder(self.config)
        self.self_prompting = SelfPromptingEngine(self.config)
        
        # Output generators
        self.pdf_generator = PDFReportGenerator(self.config)
        self.json_exporter = JSONExporter(self.config)
        self.graph_exporter = GraphExporter(self.config)
    
    def create_case(
        self,
        case_id: str,
        name: str,
        description: str = "",
        metadata: Optional[Dict] = None
    ) -> Dict:
        """
        Create a new investigation case.
        
        Args:
            case_id: Unique identifier for the case
            name: Human-readable case name
            description: Case description
            metadata: Additional metadata
            
        Returns:
            Case information dictionary
        """
        case_dir = Path(self.config["system"]["case_dir"]) / case_id
        case_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        (case_dir / "raw").mkdir(exist_ok=True)
        (case_dir / "normalized").mkdir(exist_ok=True)
        (case_dir / "analysis").mkdir(exist_ok=True)
        (case_dir / "output").mkdir(exist_ok=True)
        
        # Create case metadata file
        case_info = {
            "case_id": case_id,
            "name": name,
            "description": description,
            "created_at": datetime.now().isoformat(),
            "status": "created",
            "metadata": metadata or {}
        }
        
        metadata_path = case_dir / "case_metadata.json"
        with open(metadata_path, 'w') as f:
            import json
            json.dump(case_info, f, indent=2)
        
        self.logger.info(f"Created case: {case_id} - {name}")
        return case_info
    
    def ingest_from_google_drive(
        self,
        folder_id: str,
        case_id: str,
        recursive: bool = True
    ) -> List[str]:
        """
        Ingest files from Google Drive.
        
        Args:
            folder_id: Google Drive folder ID
            case_id: Case to ingest files into
            recursive: Whether to process subfolders
            
        Returns:
            List of ingested file paths
        """
        self.logger.info(f"Ingesting from Google Drive folder: {folder_id}")
        
        if not hasattr(self, 'google_drive'):
            raise RuntimeError("Google Drive ingestion not enabled")
        
        files = self.google_drive.ingest_folder(
            folder_id=folder_id,
            case_id=case_id,
            recursive=recursive
        )
        
        self.logger.info(f"Ingested {len(files)} files from Google Drive")
        return files
    
    def ingest_from_dropbox(
        self,
        folder_path: str,
        case_id: str,
        recursive: bool = True
    ) -> List[str]:
        """
        Ingest files from Dropbox.
        
        Args:
            folder_path: Dropbox folder path (e.g., "/Evidence/Case001")
            case_id: Case to ingest files into
            recursive: Whether to process subfolders
            
        Returns:
            List of ingested file paths
        """
        self.logger.info(f"Ingesting from Dropbox folder: {folder_path}")
        
        if not hasattr(self, 'dropbox'):
            raise RuntimeError("Dropbox ingestion not enabled")
        
        files = self.dropbox.ingest_folder(
            folder_path=folder_path,
            case_id=case_id,
            recursive=recursive
        )
        
        self.logger.info(f"Ingested {len(files)} files from Dropbox")
        return files
    
    def ingest_from_local(
        self,
        folder_path: str,
        case_id: str,
        recursive: bool = True
    ) -> List[str]:
        """
        Ingest files from local filesystem.
        
        Args:
            folder_path: Local folder path
            case_id: Case to ingest files into
            recursive: Whether to process subfolders
            
        Returns:
            List of ingested file paths
        """
        self.logger.info(f"Ingesting from local folder: {folder_path}")
        
        files = self.local.ingest_folder(
            folder_path=folder_path,
            case_id=case_id,
            recursive=recursive
        )
        
        self.logger.info(f"Ingested {len(files)} files from local folder")
        return files
    
    def process_case(self, case_id: str) -> Dict:
        """
        Process all files in a case through the complete pipeline.
        
        Args:
            case_id: Case ID to process
            
        Returns:
            Processing results summary
        """
        self.logger.info(f"Starting processing for case: {case_id}")
        
        case_dir = Path(self.config["system"]["case_dir"]) / case_id
        raw_dir = case_dir / "raw"
        
        # Get all files to process
        files = list(raw_dir.rglob("*"))
        files = [f for f in files if f.is_file()]
        
        self.logger.info(f"Found {len(files)} files to process")
        
        results = {
            "case_id": case_id,
            "total_files": len(files),
            "processed": 0,
            "failed": 0,
            "normalized_records": 0
        }
        
        # Process each file
        from tqdm import tqdm
        for file_path in tqdm(files, desc="Processing files"):
            try:
                # Route and process file
                processed_data = self.router.process_file(file_path, case_id)
                
                # Normalize to JSON
                normalized = self.normalizer.normalize(processed_data, case_id)
                
                results["processed"] += 1
                results["normalized_records"] += len(normalized)
                
            except Exception as e:
                self.logger.error(f"Failed to process {file_path}: {e}")
                results["failed"] += 1
        
        self.logger.info(f"Processing complete: {results}")
        return results
    
    def analyze_case(self, case_id: str) -> Dict:
        """
        Run AI analysis on processed case data.
        
        Args:
            case_id: Case ID to analyze
            
        Returns:
            Analysis results
        """
        self.logger.info(f"Starting analysis for case: {case_id}")
        
        case_dir = Path(self.config["system"]["case_dir"]) / case_id
        normalized_dir = case_dir / "normalized"
        
        # Load normalized data
        normalized_data = self._load_normalized_data(normalized_dir)
        
        # Layer 1: Extraction
        self.logger.info("Running Layer 1: Extraction")
        extraction_results = self.extraction_layer.analyze(normalized_data, case_id)
        
        # Layer 2: Context
        self.logger.info("Running Layer 2: Context")
        context_results = self.context_layer.analyze(
            normalized_data,
            extraction_results,
            case_id
        )
        
        # Layer 3: Investigation
        self.logger.info("Running Layer 3: Investigation")
        investigation_results = self.investigation_layer.analyze(
            normalized_data,
            extraction_results,
            context_results,
            case_id
        )
        
        # Build mind map
        self.logger.info("Building mind map")
        mind_map = self.mind_map_builder.build(
            extraction_results,
            context_results,
            investigation_results
        )
        
        # Run self-prompting
        self.logger.info("Running self-prompting engine")
        self_prompting_results = self.self_prompting.generate(
            normalized_data,
            extraction_results,
            context_results,
            investigation_results,
            mind_map
        )
        
        # Compile results
        analysis_results = {
            "case_id": case_id,
            "timestamp": datetime.now().isoformat(),
            "extraction": extraction_results,
            "context": context_results,
            "investigation": investigation_results,
            "mind_map": mind_map,
            "self_prompting": self_prompting_results
        }
        
        # Save analysis results
        analysis_file = case_dir / "analysis" / "analysis_results.json"
        with open(analysis_file, 'w') as f:
            import json
            json.dump(analysis_results, f, indent=2)
        
        self.logger.info("Analysis complete")
        return analysis_results
    
    def generate_report(
        self,
        case_id: str,
        output_format: List[str] = ["pdf", "json", "graph"]
    ) -> Dict[str, str]:
        """
        Generate investigation report.
        
        Args:
            case_id: Case ID to generate report for
            output_format: List of output formats (pdf, json, graph)
            
        Returns:
            Dictionary mapping format to output file path
        """
        self.logger.info(f"Generating report for case: {case_id}")
        
        case_dir = Path(self.config["system"]["case_dir"]) / case_id
        analysis_file = case_dir / "analysis" / "analysis_results.json"
        
        # Load analysis results
        with open(analysis_file, 'r') as f:
            import json
            analysis_results = json.load(f)
        
        output_paths = {}
        
        # Generate PDF report
        if "pdf" in output_format:
            self.logger.info("Generating PDF report")
            pdf_path = self.pdf_generator.generate(analysis_results, case_id)
            output_paths["pdf"] = str(pdf_path)
        
        # Export JSON
        if "json" in output_format:
            self.logger.info("Exporting JSON")
            json_paths = self.json_exporter.export(analysis_results, case_id)
            output_paths["json"] = json_paths
        
        # Export graph data
        if "graph" in output_format:
            self.logger.info("Exporting graph data")
            graph_paths = self.graph_exporter.export(
                analysis_results["mind_map"],
                case_id
            )
            output_paths["graph"] = graph_paths
        
        self.logger.info(f"Report generation complete: {output_paths}")
        return output_paths
    
    def _load_normalized_data(self, normalized_dir: Path) -> List[Dict]:
        """Load all normalized JSON records from directory."""
        import json
        data = []
        
        for json_file in normalized_dir.glob("*.json"):
            with open(json_file, 'r') as f:
                records = json.load(f)
                if isinstance(records, list):
                    data.extend(records)
                else:
                    data.append(records)
        
        return data


# CLI Interface
@click.group()
def cli():
    """Investigation Intelligence System CLI"""
    pass


@cli.command()
@click.option('--name', required=True, help='Case name')
@click.option('--id', 'case_id', required=True, help='Case ID')
@click.option('--description', default='', help='Case description')
def create_case(name: str, case_id: str, description: str):
    """Create a new investigation case"""
    system = InvestigationSystem()
    case_info = system.create_case(case_id, name, description)
    click.echo(f"✅ Created case: {case_id}")
    click.echo(f"   Name: {name}")


@cli.command()
@click.option('--source', required=True, type=click.Choice(['google_drive', 'dropbox', 'local']))
@click.option('--path', help='Path/folder ID')
@click.option('--folder-id', help='Google Drive folder ID')
@click.option('--case-id', required=True, help='Case ID')
@click.option('--recursive/--no-recursive', default=True)
def ingest(source: str, path: str, folder_id: str, case_id: str, recursive: bool):
    """Ingest files from various sources"""
    system = InvestigationSystem()
    
    if source == 'google_drive':
        if not folder_id:
            click.echo("❌ --folder-id required for Google Drive")
            return
        files = system.ingest_from_google_drive(folder_id, case_id, recursive)
    elif source == 'dropbox':
        if not path:
            click.echo("❌ --path required for Dropbox")
            return
        files = system.ingest_from_dropbox(path, case_id, recursive)
    elif source == 'local':
        if not path:
            click.echo("❌ --path required for local")
            return
        files = system.ingest_from_local(path, case_id, recursive)
    
    click.echo(f"✅ Ingested {len(files)} files")


@cli.command()
@click.option('--case-id', required=True, help='Case ID')
def process(case_id: str):
    """Process all files in a case"""
    system = InvestigationSystem()
    results = system.process_case(case_id)
    click.echo(f"✅ Processed {results['processed']} files")
    click.echo(f"   Failed: {results['failed']}")
    click.echo(f"   Records: {results['normalized_records']}")


@cli.command()
@click.option('--case-id', required=True, help='Case ID')
def analyze(case_id: str):
    """Run AI analysis on case"""
    system = InvestigationSystem()
    system.analyze_case(case_id)
    click.echo(f"✅ Analysis complete for case: {case_id}")


@cli.command()
@click.option('--case-id', required=True, help='Case ID')
@click.option('--format', 'output_format', multiple=True, default=['pdf', 'json', 'graph'])
@click.option('--output', help='Output directory')
def report(case_id: str, output_format: tuple, output: str):
    """Generate investigation report"""
    system = InvestigationSystem()
    paths = system.generate_report(case_id, list(output_format))
    click.echo(f"✅ Report generated:")
    for format_type, path in paths.items():
        click.echo(f"   {format_type}: {path}")


@cli.command()
@click.option('--case-id', required=True, help='Case ID')
def full_pipeline(case_id: str):
    """Run complete pipeline: process → analyze → report"""
    system = InvestigationSystem()
    
    click.echo("Step 1/3: Processing files...")
    system.process_case(case_id)
    
    click.echo("Step 2/3: Running analysis...")
    system.analyze_case(case_id)
    
    click.echo("Step 3/3: Generating report...")
    paths = system.generate_report(case_id)
    
    click.echo(f"✅ Complete! Report: {paths.get('pdf')}")


if __name__ == "__main__":
    cli()
