
from pathlib import Path
import subprocess
import sys
import logging
from datetime import datetime


# --------------------------------------------------
# 1. PROJECT CONFIGURATION
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_FOLDER = PROJECT_ROOT / "src"
LOGS_FOLDER = PROJECT_ROOT / "logs"

LOGS_FOLDER.mkdir(parents=True, exist_ok=True)

log_file = LOGS_FOLDER / (
    f"pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)

logger = logging.getLogger(__name__)


# --------------------------------------------------
# 2. PIPELINE STAGES
# --------------------------------------------------

PIPELINE_STAGES = [
    ("API Extraction", "api_extraction.py"),
    ("Data Profiling", "data_profiling.py"),
    ("Data Cleaning", "data_cleaning.py"),
    ("Data Validation", "validate_data.py"),
    ("Exploratory Data Analysis", "eda.py"),
    ("Business Insight Generation", "insight_generation.py"),
    ("HTML Report Generation", "report_generation.py"),
]


def run_stage(stage_name, script_name):
    """Execute one pipeline stage and stop if it fails."""

    script_path = SRC_FOLDER / script_name

    if not script_path.exists():
        raise FileNotFoundError(
            f"Cannot find {stage_name} script: {script_path}"
        )

    logger.info("=" * 60)
    logger.info("STARTING: %s", stage_name)
    logger.info("=" * 60)

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=str(PROJECT_ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )

    if result.stdout:
        logger.info("%s output:\n%s", stage_name, result.stdout.rstrip())

    if result.stderr:
        logger.warning(
            "%s messages:\n%s",
            stage_name,
            result.stderr.rstrip(),
        )

    if result.returncode != 0:
        logger.error(
            "%s failed with exit code %s.",
            stage_name,
            result.returncode,
        )
        raise RuntimeError(
            f"Pipeline stopped because {stage_name} failed."
        )

    logger.info("COMPLETED: %s", stage_name)


# --------------------------------------------------
# 3. MAIN PIPELINE
# --------------------------------------------------

def main():
    """Run the automated analytics pipeline."""

    start_time = datetime.now()

    print("\n" + "=" * 60)
    print("       AUTOMATED ANALYTICS PIPELINE")
    print("=" * 60)

    logger.info("Pipeline started at %s", start_time)


    

    try:
        for stage_name, script_name in PIPELINE_STAGES:
            run_stage(stage_name, script_name)

        elapsed = datetime.now() - start_time

        print("\n" + "=" * 60)
        print("PIPELINE COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print(f"Total execution time: {elapsed}")
        print(f"Log file: {log_file}")
        print(f"Reports folder: {PROJECT_ROOT / 'reports'}")
        print(f"Charts folder: {PROJECT_ROOT / 'charts'}")

        logger.info("Pipeline completed successfully in %s", elapsed)

    except Exception:
        logger.exception("Pipeline failed.")
        print("\nPIPELINE FAILED. Check the log file for details.")
        print(f"Log file: {log_file}")
        raise


if __name__ == "__main__":
    main()
