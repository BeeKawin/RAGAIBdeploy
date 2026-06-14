"""
config/settings.py
Central configuration: paths, model settings, scraper settings, and curriculum maps.
"""

import os
from pathlib import Path
from typing import Dict, List, Optional

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")
load_dotenv()


def _csv_env(name: str, default: str) -> List[str]:
    values = [value.strip() for value in os.getenv(name, default).split(",")]
    return [value for value in values if value]

# Project paths
DATA_DIR   = BASE_DIR / "data"
RAW_DIR    = DATA_DIR / "raw"
NORMALIZED_DIR = DATA_DIR / "normalized"
PROCESSED_DIR = DATA_DIR / "processed"
VECTOR_DB_DIR = BASE_DIR / "vector_db"

for _d in [RAW_DIR, NORMALIZED_DIR, PROCESSED_DIR, VECTOR_DB_DIR]:
    _d.mkdir(parents=True, exist_ok=True)

# API keys
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
OPENROUTER_SITE_URL = os.getenv("OPENROUTER_SITE_URL", "http://localhost")
OPENROUTER_APP_NAME = os.getenv("OPENROUTER_APP_NAME", "RAGAI-B-Evaluation")
ALLOWED_ORIGINS = _csv_env("ALLOWED_ORIGINS", "*")

# LLM and embedding settings
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini")   # "gemini" | "ollama" | "openrouter"
LLM_MODEL    = os.getenv("LLM_MODEL", "gemini-2.5-flash-lite")

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "BAAI/bge-m3",
)
EMBEDDING_DIMENSION = int(os.getenv("EMBEDDING_DIMENSION", "1024"))

# Vector store settings
VECTOR_STORE_TYPE  = "chroma"
CHROMA_COLLECTION  = os.getenv("CHROMA_COLLECTION", "ragaib_bge_m3_v1")
TOP_K_RETRIEVAL    = 6
SIMILARITY_THRESHOLD = 0.35

# Chunking settings
CHUNK_SIZE    = 800    # characters
CHUNK_OVERLAP = 150

# Scraper settings
SCRAPE_DELAY_SECONDS = 2.0
SCRAPE_MAX_RETRIES   = 3
SCRAPE_TIMEOUT       = 30
SCRAPE_USER_AGENT    = (
    "Mozilla/5.0 (compatible; EduBot-TH/1.0; +https://example.com/bot)"
)

OPENSTAX_CURRICULUM: List[Dict] = [{'subject': 'biology',
  'grade': 'M4',
  'topic': 'Biochemistry and Biomolecules',
  'source_url': 'https://openstax.org/books/biology-2e/pages/3-introduction'},
 {'subject': 'biology',
  'grade': 'M4',
  'topic': 'Cell Biology',
  'source_url': 'https://openstax.org/books/biology-2e/pages/4-introduction'},
 {'subject': 'biology',
  'grade': 'M4',
  'topic': 'Cellular Respiration',
  'source_url': 'https://openstax.org/books/biology-2e/pages/7-introduction'},
 {'subject': 'biology',
  'grade': 'M4',
  'topic': 'Enzymes',
  'source_url': 'https://openstax.org/books/biology-2e/pages/6-5-enzymes'},
 {'subject': 'biology',
  'grade': 'M4',
  'topic': 'Mitosis and Meiosis',
  'source_url': 'https://openstax.org/books/biology-2e/pages/10-introduction'},
 {'subject': 'biology',
  'grade': 'M4',
  'topic': 'Photosynthesis',
  'source_url': 'https://openstax.org/books/biology-2e/pages/8-introduction'},
 {'subject': 'biology',
  'grade': 'M5',
  'topic': 'DNA Structure and Replication',
  'source_url': 'https://openstax.org/books/biology-2e/pages/14-3-basics-of-dna-replication'},
 {'subject': 'biology',
  'grade': 'M5',
  'topic': 'Evolution and Natural Selection',
  'source_url': 'https://openstax.org/books/biology-2e/pages/18-introduction'},
 {'subject': 'biology',
  'grade': 'M5',
  'topic': 'Gene Expression',
  'source_url': 'https://openstax.org/books/biology-2e/pages/16-introduction'},
 {'subject': 'biology',
  'grade': 'M5',
  'topic': 'Mendelian Genetics',
  'source_url': 'https://openstax.org/books/biology-2e/pages/12-introduction'},
 {'subject': 'biology',
  'grade': 'M6',
  'topic': 'Biotechnology',
  'source_url': 'https://openstax.org/books/biology-2e/pages/17-introduction'},
 {'subject': 'biology',
  'grade': 'M6',
  'topic': 'Ecology and Ecosystems',
  'source_url': 'https://openstax.org/books/biology-2e/pages/44-introduction'},
 {'subject': 'biology',
  'grade': 'M6',
  'topic': 'Human Body Systems',
  'source_url': 'https://openstax.org/books/biology-2e/pages/33-introduction'},
 {'subject': 'biology',
  'grade': 'M6',
  'topic': 'Immune System',
  'source_url': 'https://openstax.org/books/biology-2e/pages/42-introduction'},
 {'subject': 'biology',
  'grade': 'M6',
  'topic': 'Nervous and Endocrine Systems',
  'source_url': 'https://openstax.org/books/biology-2e/pages/35-introduction'},
 {'subject': 'biology',
  'grade': 'M6',
  'topic': 'Plant Biology',
  'source_url': 'https://openstax.org/books/biology-2e/pages/30-introduction'},
 {'subject': 'chemistry',
  'grade': 'M4',
  'topic': 'Atomic Structure',
  'source_url': 'https://openstax.org/books/chemistry-2e/pages/2-2-evolution-of-atomic-theory'},
 {'subject': 'chemistry',
  'grade': 'M4',
  'topic': 'Chemical Bonding',
  'source_url': 'https://openstax.org/books/chemistry-2e/pages/7-introduction'},
 {'subject': 'chemistry',
  'grade': 'M4',
  'topic': 'Electron Configuration',
  'source_url': 'https://openstax.org/books/chemistry-2e/pages/6-4-electronic-structure-of-atoms-electron-configurations'},
 {'subject': 'chemistry',
  'grade': 'M4',
  'topic': 'Intermolecular Forces',
  'source_url': 'https://openstax.org/books/chemistry-2e/pages/10-1-intermolecular-forces'},
 {'subject': 'chemistry',
  'grade': 'M4',
  'topic': 'Ionic and Covalent Bonds',
  'source_url': 'https://openstax.org/books/chemistry-2e/pages/7-2-covalent-bonding'},
 {'subject': 'chemistry',
  'grade': 'M4',
  'topic': 'Periodic Table and Trends',
  'source_url': 'https://openstax.org/books/chemistry-2e/pages/6-5-periodic-variations-in-element-properties'},
 {'subject': 'chemistry',
  'grade': 'M4',
  'topic': 'Stoichiometry',
  'source_url': 'https://openstax.org/books/chemistry-2e/pages/4-3-reaction-stoichiometry'},
 {'subject': 'chemistry',
  'grade': 'M5',
  'topic': 'Acids and Bases',
  'source_url': 'https://openstax.org/books/chemistry-2e/pages/14-2-ph-and-poh'},
 {'subject': 'chemistry',
  'grade': 'M5',
  'topic': 'Electrochemistry',
  'source_url': 'https://openstax.org/books/chemistry-2e/pages/17-introduction'},
 {'subject': 'chemistry',
  'grade': 'M5',
  'topic': 'Gas Laws',
  'source_url': 'https://openstax.org/books/chemistry-2e/pages/9-2-relating-pressure-volume-amount-and-temperature-the-ideal-gas-law'},
 {'subject': 'chemistry',
  'grade': 'M5',
  'topic': 'Solutions and Concentration',
  'source_url': 'https://openstax.org/books/chemistry-2e/pages/11-3-solubility'},
 {'subject': 'chemistry',
  'grade': 'M5',
  'topic': 'pH and Buffers',
  'source_url': 'https://openstax.org/books/chemistry-2e/pages/14-6-buffers'},
 {'subject': 'chemistry',
  'grade': 'M6',
  'topic': 'Chemical Equilibrium',
  'source_url': 'https://openstax.org/books/chemistry-2e/pages/13-introduction'},
 {'subject': 'chemistry',
  'grade': 'M6',
  'topic': 'Chemical Kinetics',
  'source_url': 'https://openstax.org/books/chemistry-2e/pages/12-introduction'},
 {'subject': 'chemistry',
  'grade': 'M6',
  'topic': 'Functional Groups',
  'source_url': 'https://openstax.org/books/organic-chemistry/pages/3-1-functional-groups'},
 {'subject': 'chemistry',
  'grade': 'M6',
  'topic': 'Polymers',
  'source_url': 'https://openstax.org/books/chemistry-2e/pages/10-6-lattice-structures-in-crystalline-solids'},
 {'subject': 'chemistry',
  'grade': 'M6',
  'topic': 'Thermochemistry',
  'source_url': 'https://openstax.org/books/chemistry-2e/pages/5-introduction'},
 {'subject': 'math',
  'grade': 'M4',
  'topic': 'Exponential Functions',
  'source_url': 'https://openstax.org/books/algebra-and-trigonometry-2e/pages/6-1-exponential-functions'},
 {'subject': 'math',
  'grade': 'M4',
  'topic': 'Linear Equations and Inequalities',
  'source_url': 'https://openstax.org/books/algebra-and-trigonometry-2e/pages/2-2-linear-equations-in-one-variable'},
 {'subject': 'math',
  'grade': 'M4',
  'topic': 'Logarithms',
  'source_url': 'https://openstax.org/books/algebra-and-trigonometry-2e/pages/6-3-logarithmic-functions'},
 {'subject': 'math',
  'grade': 'M4',
  'topic': 'Logic and Reasoning',
  'source_url': 'https://openstax.org/books/contemporary-mathematics/pages/2-2-compound-statements'},
 {'subject': 'math',
  'grade': 'M4',
  'topic': 'Quadratic Equations',
  'source_url': 'https://openstax.org/books/algebra-and-trigonometry-2e/pages/2-5-quadratic-equations'},
 {'subject': 'math',
  'grade': 'M4',
  'topic': 'Real Number System',
  'source_url': 'https://openstax.org/books/algebra-and-trigonometry-2e/pages/1-1-real-numbers-algebra-essentials'},
 {'subject': 'math',
  'grade': 'M4',
  'topic': 'Relations and Functions',
  'source_url': 'https://openstax.org/books/algebra-and-trigonometry-2e/pages/3-1-functions-and-function-notation'},
 {'subject': 'math',
  'grade': 'M4',
  'topic': 'Sets',
  'source_url': 'https://openstax.org/books/contemporary-mathematics/pages/1-4-set-operations-with-two-sets'},
 {'subject': 'math',
  'grade': 'M5',
  'topic': 'Arithmetic Sequences',
  'source_url': 'https://openstax.org/books/algebra-and-trigonometry-2e/pages/13-2-arithmetic-sequences'},
 {'subject': 'math',
  'grade': 'M5',
  'topic': 'Conic Sections',
  'source_url': 'https://openstax.org/books/algebra-and-trigonometry-2e/pages/12-introduction-to-analytic-geometry'},
 {'subject': 'math',
  'grade': 'M5',
  'topic': 'Geometric Sequences',
  'source_url': 'https://openstax.org/books/algebra-and-trigonometry-2e/pages/13-3-geometric-sequences'},
 {'subject': 'math',
  'grade': 'M5',
  'topic': 'Permutations and Combinations',
  'source_url': 'https://openstax.org/books/precalculus/pages/11-5-counting-principles'},
 {'subject': 'math',
  'grade': 'M5',
  'topic': 'Statistics and Probability',
  'source_url': 'https://openstax.org/books/introductory-statistics-2e/pages/3-introduction'},
 {'subject': 'math',
  'grade': 'M5',
  'topic': 'Trigonometric Functions',
  'source_url': 'https://openstax.org/books/algebra-and-trigonometry-2e/pages/7-2-right-triangle-trigonometry'},
 {'subject': 'math',
  'grade': 'M5',
  'topic': 'Trigonometric Identities',
  'source_url': 'https://openstax.org/books/algebra-and-trigonometry-2e/pages/9-1-verifying-trigonometric-identities-and-using-trigonometric-identities-to-simplify-trigonometric-expressions'},
 {'subject': 'math',
  'grade': 'M6',
  'topic': 'Derivatives',
  'source_url': 'https://openstax.org/books/calculus-volume-1/pages/3-1-defining-the-derivative'},
 {'subject': 'math',
  'grade': 'M6',
  'topic': 'Integrals',
  'source_url': 'https://openstax.org/books/calculus-volume-1/pages/5-2-the-definite-integral'},
 {'subject': 'math',
  'grade': 'M6',
  'topic': 'Limits',
  'source_url': 'https://openstax.org/books/calculus-volume-1/pages/2-2-the-limit-of-a-function'},
 {'subject': 'math',
  'grade': 'M6',
  'topic': 'Matrices',
  'source_url': 'https://openstax.org/books/precalculus/pages/9-5-matrices-and-matrix-operations'},
 {'subject': 'math',
  'grade': 'M6',
  'topic': 'Vectors',
  'source_url': 'https://openstax.org/books/algebra-and-trigonometry-2e/pages/10-8-vectors'},
 {'subject': 'physics',
  'grade': 'M4',
  'topic': 'Circular Motion',
  'source_url': 'https://openstax.org/books/college-physics-2e/pages/6-introduction-to-uniform-circular-motion-and-gravitation'},
 {'subject': 'physics',
  'grade': 'M4',
  'topic': 'Kinematics 1D',
  'source_url': 'https://openstax.org/books/college-physics-2e/pages/2-introduction-to-one-dimensional-kinematics'},
 {'subject': 'physics',
  'grade': 'M4',
  'topic': 'Kinematics 2D',
  'source_url': 'https://openstax.org/books/college-physics-2e/pages/3-introduction-to-two-dimensional-kinematics'},
 {'subject': 'physics',
  'grade': 'M4',
  'topic': 'Measurement and Units',
  'source_url': 'https://openstax.org/books/college-physics-2e/pages/1-2-physical-quantities-and-units'},
 {'subject': 'physics',
  'grade': 'M4',
  'topic': 'Momentum and Collisions',
  'source_url': 'https://openstax.org/books/college-physics-2e/pages/8-introduction-to-linear-momentum-and-collisions'},
 {'subject': 'physics',
  'grade': 'M4',
  'topic': "Newton's Laws of Motion",
  'source_url': 'https://openstax.org/books/college-physics-2e/pages/4-3-newtons-second-law-of-motion-concept-of-a-system'},
 {'subject': 'physics',
  'grade': 'M4',
  'topic': 'Work Energy and Power',
  'source_url': 'https://openstax.org/books/college-physics-2e/pages/7-introduction-to-work-energy-and-energy-resources'},
 {'subject': 'physics',
  'grade': 'M5',
  'topic': 'Gravitation',
  'source_url': 'https://openstax.org/books/college-physics-2e/pages/6-5-newtons-universal-law-of-gravitation'},
 {'subject': 'physics',
  'grade': 'M5',
  'topic': 'Heat Transfer',
  'source_url': 'https://openstax.org/books/college-physics-2e/pages/14-introduction-to-heat-and-heat-transfer-methods'},
 {'subject': 'physics',
  'grade': 'M5',
  'topic': 'Rotational Motion',
  'source_url': 'https://openstax.org/books/college-physics-2e/pages/10-introduction-to-rotational-motion-and-angular-momentum'},
 {'subject': 'physics',
  'grade': 'M5',
  'topic': 'Simple Harmonic Motion',
  'source_url': 'https://openstax.org/books/college-physics-2e/pages/16-3-simple-harmonic-motion-a-special-periodic-motion'},
 {'subject': 'physics',
  'grade': 'M5',
  'topic': 'Thermodynamics',
  'source_url': 'https://openstax.org/books/college-physics-2e/pages/15-introduction-to-thermodynamics'},
 {'subject': 'physics',
  'grade': 'M5',
  'topic': 'Waves and Sound',
  'source_url': 'https://openstax.org/books/college-physics-2e/pages/16-introduction-to-oscillatory-motion-and-waves'},
 {'subject': 'physics',
  'grade': 'M6',
  'topic': 'Electric Current and Circuits',
  'source_url': 'https://openstax.org/books/college-physics-2e/pages/20-introduction-to-electric-current-resistance-and-ohms-law'},
 {'subject': 'physics',
  'grade': 'M6',
  'topic': 'Electromagnetic Induction',
  'source_url': 'https://openstax.org/books/college-physics-2e/pages/23-introduction-to-electromagnetic-induction-ac-circuits-and-electrical-technologies'},
 {'subject': 'physics',
  'grade': 'M6',
  'topic': 'Electrostatics',
  'source_url': 'https://openstax.org/books/college-physics-2e/pages/18-introduction-to-electric-charge-and-electric-field'},
 {'subject': 'physics',
  'grade': 'M6',
  'topic': 'Light and Optics',
  'source_url': 'https://openstax.org/books/college-physics-2e/pages/25-introduction-to-geometric-optics'},
 {'subject': 'physics',
  'grade': 'M6',
  'topic': 'Magnetism',
  'source_url': 'https://openstax.org/books/college-physics-2e/pages/22-introduction-to-magnetism'},
 {'subject': 'physics',
  'grade': 'M6',
  'topic': 'Nuclear Physics',
  'source_url': 'https://openstax.org/books/college-physics-2e/pages/31-introduction-to-radioactivity-and-nuclear-physics'},
 {'subject': 'physics',
  'grade': 'M6',
  'topic': 'Quantum Physics',
  'source_url': 'https://openstax.org/books/college-physics-2e/pages/29-introduction-to-quantum-physics'}]

# SciMath Curriculum Map - Thailand High-School M4-M6
SCIMATH_CURRICULUM: List[Dict] = [
    # Mathematics 35 Entries
    {
        "subject": "mathematics",
        "grade": "M6",
        "topic": 'คณิตศาสตร์การเงิน',
        "scimath_url": "https://www.scimath.org/lesson-mathematics/item/11532-2020-05-01-03-18-05"
    },
    {
        "subject": "mathematics",
        "grade": "M5",
        "topic": 'ฟังก์ชันและฟังก์ชันในคอมพิวเตอร์',
        "scimath_url": "https://www.scimath.org/lesson-mathematics/item/9779-2019-02-21-06-19-23"
    },
    {
        "subject": "mathematics",
        "grade": "M4",
        "topic": 'คณิตศาสตร์ด้านการจัดหมู่',
        "scimath_url": "https://www.scimath.org/lesson-mathematics/item/11244-2019-12-19-07-31-43"
    },
    {
        "subject": "mathematics",
        "grade": "M5",
        "topic": 'ลำดับและอนุกรมและการประยุกต์',
        "scimath_url": "https://www.scimath.org/lesson-mathematics/item/11531-2020-05-01-03-14-46"
    },
    {
        "subject": "mathematics",
        "grade": "M6",
        "topic": 'เรขาคณิตขั้นสูงระดับมัธยมปลาย',
        "scimath_url": "https://www.scimath.org/lesson-mathematics/item/11675-2020-06-30-07-34-18"
    },
    {
        "subject": "mathematics",
        "grade": "M5",
        "topic": 'ฟังก์ชันพีชคณิตและกราฟ',
        "scimath_url": "https://www.scimath.org/lesson-mathematics/item/11002-2019-10-28-07-17-08"
    },
    {
        "subject": "mathematics",
        "grade": "M5",
        "topic": 'ความสัมพันธ์เชิงฟังก์ชันระหว่างข้อมูล',
        "scimath_url": "https://www.scimath.org/lesson-mathematics/item/11311-2020-02-18-04-02-24"
    },
    {
        "subject": "mathematics",
        "grade": "M4",
        "topic": 'ตรรกศาสตร์กับคอมพิวเตอร์',
        "scimath_url": "https://www.scimath.org/lesson-mathematics/item/8789-2018-09-21-01-56-47"
    },
    {
        "subject": "mathematics",
        "grade": "M6",
        "topic": 'สมการไดโอแฟนไทน์เชิงเส้น (Linear Diophantine Equations)',
        "scimath_url": "https://www.scimath.org/lesson-mathematics/item/7362-linear-diophantine-equations"
    },
    {
        "subject": "mathematics",
        "grade": "M4",
        "topic": 'การแก้อสมการ',
        "scimath_url": "https://www.scimath.org/lesson-mathematics/item/7357-2017-06-18-04-46-43"
    },
    {
        "subject": "mathematics",
        "grade": "M4",
        "topic": 'ความสัมพันธ์เชิงคณิตศาสตร์',
        "scimath_url": "https://www.scimath.org/lesson-mathematics/item/9625-2018-12-14-05-55-26"
    },
    {
        "subject": "mathematics",
        "grade": "M6",
        "topic": 'เรขาคณิตหลายมิติ',
        "scimath_url": "https://www.scimath.org/lesson-mathematics/item/7348-2017-06-18-04-32-23"
    },
    {
        "subject": "mathematics",
        "grade": "M4",
        "topic": 'ตรรกศาสตร์',
        "scimath_url": "https://www.scimath.org/lesson-mathematics/item/8787-2018-09-21-01-54-19"
    },
    {
        "subject": "mathematics",
        "grade": "M4",
        "topic": 'การให้เหตุผล',
        "scimath_url": "https://www.scimath.org/lesson-mathematics/item/7332-2017-06-17-08-40-43"
    },
    {
        "subject": "mathematics",
        "grade": "M5",
        "topic": 'อนุกรมที่น่าสนใจ',
        "scimath_url": "https://www.scimath.org/lesson-mathematics/item/7343-2017-06-18-03-58-14"
    },
    {
        "subject": "mathematics",
        "grade": "M6",
        "topic": 'ภาคตัดกรวย',
        "scimath_url": "https://www.scimath.org/lesson-mathematics/item/7333-2017-06-17-08-44-23"
    },
    {
        "subject": "mathematics",
        "grade": "M4",
        "topic": 'ทฤษฎีกราฟเบื้องต้น',
        "scimath_url": "https://www.scimath.org/lesson-mathematics/item/7334-2017-06-17-14-37-32"
    },
    {
        "subject": "mathematics",
        "grade": "M5",
        "topic": 'ฟังก์ชันตรีโกณมิติ',
        "scimath_url": "https://www.scimath.org/lesson-mathematics/item/7346-2017-06-18-04-21-28"
    },
    {
        "subject": "mathematics",
        "grade": "M5",
        "topic": 'ฟังก์ชัน',
        "scimath_url": "https://www.scimath.org/lesson-mathematics/item/7335-2017-06-17-14-47-42"
    },
    {
        "subject": "mathematics",
        "grade": "M6",
        "topic": 'ปริภูมิสามมิติ',
        "scimath_url": "https://www.scimath.org/lesson-mathematics/item/7329-2017-06-17-08-07-43"
    },
    {
        "subject": "mathematics",
        "grade": "M4",
        "topic": 'เซต (Set)',
        "scimath_url": "https://www.scimath.org/lesson-mathematics/item/7065-set"
    },
    {
        "subject": "mathematics",
        "grade": "M6",
        "topic": 'เทคนิคการอินทิเกรต และการประยุกต์',
        "scimath_url": "https://www.scimath.org/lesson-mathematics/item/7327-2017-06-17-07-52-52"
    },
    {
        "subject": "mathematics",
        "grade": "M6",
        "topic": 'ทฤษฎีจำนวนเบื้องต้น',
        "scimath_url": "https://www.scimath.org/lesson-mathematics/item/7330-2017-06-17-08-11-53"
    },
    {
        "subject": "mathematics",
        "grade": "M6",
        "topic": 'กำหนดการเชิงเส้น',
        "scimath_url": "https://www.scimath.org/lesson-mathematics/item/7326-2017-06-17-07-50-09"
    },
    {
        "subject": "mathematics",
        "grade": "M6",
        "topic": 'จำนวนเชิงซ้อน',
        "scimath_url": "https://www.scimath.org/lesson-mathematics/item/7066-2"
    },
    {
        "subject": "mathematics",
        "grade": "M6",
        "topic": 'แคลคูลัสเบื้องต้น',
        "scimath_url": "https://www.scimath.org/lesson-mathematics/item/7324-2017-06-17-06-14-55"
    },
    {
        "subject": "mathematics",
        "grade": "M5",
        "topic": 'ความน่าจะเป็น เรียนรู้จากตัวอย่าง',
        "scimath_url": "https://www.scimath.org/lesson-mathematics/item/7328-2017-06-17-08-01-14"
    },
    {
        "subject": "mathematics",
        "grade": "M6",
        "topic": 'สถิติ (Statistics)',
        "scimath_url": "https://www.scimath.org/lesson-mathematics/item/7067-statistics"
    },
    {
        "subject": "mathematics",
        "grade": "M6",
        "topic": "Advanced Mathematics",
        "scimath_url": "https://www.scimath.org/lesson-mathematics/item/7331-advanced-mathematics"
    },
    {
        "subject": "mathematics",
        "grade": "M5",
        "topic": 'ลำดับ และอนุกรม (Sequences & Series)',
        "scimath_url": "https://www.scimath.org/lesson-mathematics/item/7068-sequences-series"
    },
    {
        "subject": "mathematics",
        "grade": "M5",
        "topic": 'ตรีโกณ',
        "scimath_url": "https://www.scimath.org/lesson-mathematics/item/7060-2017-05-24-15-21-17"
    },
    {
        "subject": "mathematics",
        "grade": "M5",
        "topic": 'เวกเตอร์ (Vector)',
        "scimath_url": "https://www.scimath.org/lesson-mathematics/item/7057-vector-7057"
    },
    {
        "subject": "mathematics",
        "grade": "M4",
        "topic": 'ช่วงและการแก้อสมการ ช่วงและการแก้อสมการ',
        "scimath_url": "https://www.scimath.org/lesson-mathematics/item/7063-2017-05-25-14-45-11"
    },
    {
        "subject": "mathematics",
        "grade": "M4",
        "topic": 'ระบบจำนวนจริง',
        "scimath_url": "https://www.scimath.org/lesson-mathematics/item/7058-2017-05-24-14-59-48"
    },
    {
        "subject": "mathematics",
        "grade": "M4",
        "topic": 'การแก้สมการตัวแปรเดียว',
        "scimath_url": "https://www.scimath.org/lesson-mathematics/item/7062-2017-05-25-14-38-58"
    },

    # Chemistry 87 Entries

    {
        "subject": "chemistry",
        "grade": "M5",
        "topic": 'สารละลาย',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/11241-2019-12-19-07-24-03"
    },
    {
        "subject": "chemistry",
        "grade": "M6",
        "topic": 'สารประกอบไฮโดรคาร์บอนอิ่มตัว',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/9786-2019-02-21-06-33-22"
    },
    {
        "subject": "chemistry",
        "grade": "M6",
        "topic": 'เซลล์ไฟฟ้าเคมีและความก้าวหน้าทางเทคโนโลยีที่เกี่ยวข้อง',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/10321-2019-05-13-05-59-15"
    },
    {
        "subject": "chemistry",
        "grade": "M5",
        "topic": 'สมดุลเคมี',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/11676-2020-06-30-07-35-26"
    },
    {
        "subject": "chemistry",
        "grade": "M4",
        "topic": 'การเปลี่ยนแปลงทางเคมี',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/9785-2019-02-21-06-31-14"
    },
    {
        "subject": "chemistry",
        "grade": "M6",
        "topic": 'เซลล์ไฟฟ้าเบื้องต้น',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/9788-2019-02-21-06-37-12"
    },
    {
        "subject": "chemistry",
        "grade": "M5",
        "topic": 'สารละลายกรด เบส',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/10557-2019-08-28-02-17-52"
    },
    {
        "subject": "chemistry",
        "grade": "M4",
        "topic": 'โครงสร้างอะตอม',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/10318-2019-05-13-05-54-21"
    },
    {
        "subject": "chemistry",
        "grade": "M6",
        "topic": 'เซลล์ไฟฟ้าเคมี',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/11310-2020-02-18-03-57-00"
    },
    {
        "subject": "chemistry",
        "grade": "M4",
        "topic": 'ประโยชน์ของสารในชีวิตประจำวัน',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/11533-2020-05-01-03-28-11"
    },
    {
        "subject": "chemistry",
        "grade": "M4",
        "topic": 'การแยกสารเนื้อเดียว (สกัดด้วยตัวทำละลาย/ตกผลึก/กลั่น/โครมาโทกราฟี)',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/9423-2018-11-14-08-38-39"
    },
    {
        "subject": "chemistry",
        "grade": "M6",
        "topic": 'พอลิเมอร์',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/9631-1-9631"
    },
    {
        "subject": "chemistry",
        "grade": "M4",
        "topic": 'การแยกสารเนื้อผสม',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/8795-2018-09-21-02-06-13"
    },
    {
        "subject": "chemistry",
        "grade": "M6",
        "topic": 'สารประกอบอินทรีย์',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/9633-2018-12-14-05-59-34"
    },
    {
        "subject": "chemistry",
        "grade": "M5",
        "topic": 'สารละลายกรด – เบส',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7887-2018-02-27-03-53-51"
    },
    {
        "subject": "chemistry",
        "grade": "M4",
        "topic": 'ชนิดของสสารและการจำแนก',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/8798-2018-09-21-02-09-12"
    },
    {
        "subject": "chemistry",
        "grade": "M4",
        "topic": 'สารประกอบไอออนิก',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/9632-2-9632"
    },
    {
        "subject": "chemistry",
        "grade": "M4",
        "topic": 'โลหะในตารางธาตุ',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/9428-2018-11-14-08-43-08"
    },
    {
        "subject": "chemistry",
        "grade": "M6",
        "topic": 'เคมีอินทรีย์',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/9634-2018-12-14-08-26-46"
    },
    {
        "subject": "chemistry",
        "grade": "M4",
        "topic": 'โลหะ',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7198-2017-06-09-12-48-14"
    },
    {
        "subject": "chemistry",
        "grade": "M4",
        "topic": 'สมบัติของสารประกอบและธาตุ',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7196-2017-06-09-12-37-06"
    },
    {
        "subject": "chemistry",
        "grade": "M5",
        "topic": 'สารละลาย',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7195-2017-06-09-12-29-31"
    },
    {
        "subject": "chemistry",
        "grade": "M5",
        "topic": 'อินดิเคเตอร์',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7193-2017-06-08-15-20-55"
    },
    {
        "subject": "chemistry",
        "grade": "M4",
        "topic": 'แบบจำลองอะตอม',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7437-2017-08-11-04-28-08"
    },
    {
        "subject": "chemistry",
        "grade": "M4",
        "topic": 'อะตอมและตารางธาตุ 1',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7438-2017-08-11-04-30-34"
    },
    {
        "subject": "chemistry",
        "grade": "M4",
        "topic": 'สารประกอบโคเวเลนต์ (Covalent Compound)',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7202-covalent-compound"
    },
    {
        "subject": "chemistry",
        "grade": "M5",
        "topic": 'อุณหพลศาสตร์ (Thermodynamics)',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7194-thermodynamics"
    },
    {
        "subject": "chemistry",
        "grade": "M5",
        "topic": "acid-base",
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7200-acid-base"
    },
    {
        "subject": "chemistry",
        "grade": "M5",
        "topic": 'อัตราการเกิดปฏิกิริยาเคมี (Reaction rate)',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7191-reaction-rate"
    },
    {
        "subject": "chemistry",
        "grade": "M6",
        "topic": 'สารชีวโมเลกุล:โปรตีน',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7192-2017-06-08-15-15-54"
    },
    {
        "subject": "chemistry",
        "grade": "M6",
        "topic": 'เคมีอาหาร (food chemistry)',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7185-food-chemistry"
    },
    {
        "subject": "chemistry",
        "grade": "M4",
        "topic": 'แร่รัตนชาติ',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7184-2017-06-05-15-10-27"
    },
    {
        "subject": "chemistry",
        "grade": "M5",
        "topic": 'สารละลายกรด-เบส',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7189-2017-06-08-14-48-54"
    },
    {
        "subject": "chemistry",
        "grade": "M4",
        "topic": 'อะตอมและตารางธาตุ',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7180-2017-06-05-14-30-33"
    },
    {
        "subject": "chemistry",
        "grade": "M4",
        "topic": 'สารประกอบไอออนิก',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7183-2017-06-05-15-01-31"
    },
    {
        "subject": "chemistry",
        "grade": "M4",
        "topic": 'พันธะโคเวเลนต์',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7186-2017-06-08-03-20-08"
    },
    {
        "subject": "chemistry",
        "grade": "M6",
        "topic": 'การศึกษาปิโตรเลียม',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7190-2017-06-08-15-07-00"
    },
    {
        "subject": "chemistry",
        "grade": "M5",
        "topic": 'การชุบโลหะ',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7179-2017-06-05-14-14-44"
    },
    {
        "subject": "chemistry",
        "grade": "M5",
        "topic": 'การกัดกร่อนและการป้องกัน',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7182-2017-06-05-14-44-28"
    },
    {
        "subject": "chemistry",
        "grade": "M4",
        "topic": 'โมลและปริมาณต่อโมล',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7188-2017-06-08-14-39-10"
    },
    {
        "subject": "chemistry",
        "grade": "M4",
        "topic": 'แร่',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7187-2017-06-08-14-16-10"
    },
    {
        "subject": "chemistry",
        "grade": "M4",
        "topic": 'การละลาย (Solubility)',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7178-solubility"
    },
    {
        "subject": "chemistry",
        "grade": "M5",
        "topic": 'เซลล์เชื้อเพลิง (Fuel cells)',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7156-fuel-cells"
    },
    {
        "subject": "chemistry",
        "grade": "M6",
        "topic": 'ปิโตรเลียม',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7161-2017-06-04-14-39-57"
    },
    {
        "subject": "chemistry",
        "grade": "M4",
        "topic": 'พันธะเคมีหลักสูตร สอวน.',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7177-2017-06-05-14-03-17"
    },
    {
        "subject": "chemistry",
        "grade": "M4",
        "topic": 'ปฏิกิริยาเคมีและสมการเคมี',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7172-2017-06-05-13-30-08"
    },
    {
        "subject": "chemistry",
        "grade": "M6",
        "topic": 'เคมีสีเขียว (Green Chemistry)',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7167-green-chemistry"
    },
    {
        "subject": "chemistry",
        "grade": "M6",
        "topic": 'ไขมันและน้ำมัน',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7163-2017-06-04-15-11-40"
    },
    {
        "subject": "chemistry",
        "grade": "M6",
        "topic": 'ภาวะมลพิษที่เกิดจากผลิตภัณฑ์ปิโตรเคมี',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7159-2017-06-04-14-21-43"
    },
    {
        "subject": "chemistry",
        "grade": "M6",
        "topic": 'เคมีนิวเคลียร์',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7166-2017-06-04-15-54-56"
    },
    {
        "subject": "chemistry",
        "grade": "M4",
        "topic": 'ออร์บิทัล (Orbital)',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7162-orbital"
    },
    {
        "subject": "chemistry",
        "grade": "M4",
        "topic": 'โครงสร้างอะตอม',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7174-2017-06-05-13-47-55"
    },
    {
        "subject": "chemistry",
        "grade": "M4",
        "topic": 'สมบัติของธาตุและสารประกอบ',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7160-2017-06-04-14-29-21"
    },
    {
        "subject": "chemistry",
        "grade": "M5",
        "topic": 'อัตราการเกิดปฏิกิริยาเคมี (สอวน.)',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7158-2017-06-04-14-17-30"
    },
    {
        "subject": "chemistry",
        "grade": "M6",
        "topic": 'เคมีกับเซรามิกส์',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7140-2017-06-04-08-43-52"
    },
    {
        "subject": "chemistry",
        "grade": "M6",
        "topic": 'เคมีอินทรีย์ สารชีวโมเลกุล และผลิตภัณฑ์ปิโตรเลียม',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7136-2017-06-04-08-25-17"
    },
    {
        "subject": "chemistry",
        "grade": "M6",
        "topic": 'หมู่ฟังก์ชัน (functional groups)',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7154-functional-groups"
    },
    {
        "subject": "chemistry",
        "grade": "M4",
        "topic": 'เคมีพื้นฐาน',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7122-2017-06-04-07-25-22"
    },
    {
        "subject": "chemistry",
        "grade": "M5",
        "topic": 'สมดุลกรด-เบส',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7153-2017-06-04-13-31-42"
    },
    {
        "subject": "chemistry",
        "grade": "M4",
        "topic": 'แบบจำลองอะตอม (Atomic Model)',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7121-atomic-model"
    },
    {
        "subject": "chemistry",
        "grade": "M4",
        "topic": 'สมบัติของธาตุ/สารประกอบ',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7126-2017-06-04-07-48-00"
    },
    {
        "subject": "chemistry",
        "grade": "M6",
        "topic": 'การอ่านชื่อสารประกอบอินทรีย์',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7106-2017-06-04-06-29-28"
    },
    {
        "subject": "chemistry",
        "grade": "M6",
        "topic": 'สารเคมีกับเครื่องสำอาง',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7105-2017-06-04-04-20-19"
    },
    {
        "subject": "chemistry",
        "grade": "M6",
        "topic": 'ปุ๋ย',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7124-2017-06-04-07-32-46"
    },
    {
        "subject": "chemistry",
        "grade": "M6",
        "topic": 'โปรตีน',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7152-2017-06-04-13-19-27"
    },
    {
        "subject": "chemistry",
        "grade": "M5",
        "topic": 'สมดุลเคมี',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7134-2017-06-04-08-13-48"
    },
    {
        "subject": "chemistry",
        "grade": "M6",
        "topic": 'ดิน',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7098-2017-06-04-03-20-42"
    },
    {
        "subject": "chemistry",
        "grade": "M6",
        "topic": 'พอลิเมอร์ (polymer)',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7089-polymer"
    },
    {
        "subject": "chemistry",
        "grade": "M4",
        "topic": 'สารประกอบอนินทรีย์ (inorganic compound)',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7104-inorganic-compound"
    },
    {
        "subject": "chemistry",
        "grade": "M6",
        "topic": 'ไบโอแก๊ส (Biogas)',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7101-biogas"
    },
    {
        "subject": "chemistry",
        "grade": "M6",
        "topic": 'สารชีวโมเลกุล (biomolecule)',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7094-biomolecule"
    },
    {
        "subject": "chemistry",
        "grade": "M6",
        "topic": 'สารอินทรีย์',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7087-2017-05-28-03-25-53"
    },
    {
        "subject": "chemistry",
        "grade": "M6",
        "topic": 'ผลิตภัณฑ์ปิโตรเลียม',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7088-2017-05-28-03-40-32"
    },
    {
        "subject": "chemistry",
        "grade": "M5",
        "topic": 'ไฟฟ้าเคมี',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7090-2017-05-28-04-13-50"
    },
    {
        "subject": "chemistry",
        "grade": "M4",
        "topic": 'แก๊ส ของแข็ง ของเหลว',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7099-2017-06-04-03-26-32"
    },
    {
        "subject": "chemistry",
        "grade": "M6",
        "topic": 'การอ่านชื่อสารเคมี',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7100-2017-06-04-03-30-01"
    },
    {
        "subject": "chemistry",
        "grade": "M6",
        "topic": 'พอลิเมอร์',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7095-2017-06-04-02-45-14"
    },
    {
        "subject": "chemistry",
        "grade": "M6",
        "topic": 'นาโนเทคโนโลยี (Nanotechnology)',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7081-nanotechnology"
    },
    {
        "subject": "chemistry",
        "grade": "M4",
        "topic": 'ของแข็ง (Solid)',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7086-solid"
    },
    {
        "subject": "chemistry",
        "grade": "M4",
        "topic": 'สารละลาย (solution)',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7077-solution"
    },
    {
        "subject": "chemistry",
        "grade": "M4",
        "topic": 'สารและสมบัติของสาร',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7072-2017-05-26-15-27-24"
    },
    {
        "subject": "chemistry",
        "grade": "M4",
        "topic": 'ปริมาณสารสัมพันธ์',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7084-2017-05-28-02-52-54"
    },
    {
        "subject": "chemistry",
        "grade": "M5",
        "topic": 'กรด-เบส',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7071-2017-05-26-15-16-15"
    },
    {
        "subject": "chemistry",
        "grade": "M4",
        "topic": 'ตารางธาตุ',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7076-2017-05-27-14-52-36"
    },
    {
        "subject": "chemistry",
        "grade": "M5",
        "topic": 'เกลือ',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7080-2017-05-28-02-23-54"
    },
    {
        "subject": "chemistry",
        "grade": "M5",
        "topic": 'อัตราการเกิดปฏิกิริยาเคมี',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7083-2017-05-28-02-44-10"
    },
    {
        "subject": "chemistry",
        "grade": "M4",
        "topic": 'สถานะของสาร',
        "scimath_url": "https://www.scimath.org/lesson-chemistry/item/7078-2017-05-28-02-15-42"
    },

    # Physics 85 Entries
    {
        "subject": "physics",
        "grade": "M5",
        "topic": 'ไฟฟ้าและแม่เหล็ก',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/11246-2019-12-19-07-36-11"
    },
    {
        "subject": "physics",
        "grade": "M6",
        "topic": 'ไฟฟ้าสถิต ระดับชั้น ม.6',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/9622-2018-12-14-05-54-18"
    },
    {
        "subject": "physics",
        "grade": "M4",
        "topic": 'การเคลื่อนที่ในแนวตรง',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/8781-2018-09-20-06-43-41"
    },
    {
        "subject": "physics",
        "grade": "M4",
        "topic": 'แรง มวล และกฎการเคลื่อนที่',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/8782-2018-09-20-06-44-23"
    },
    {
        "subject": "physics",
        "grade": "M6",
        "topic": 'ฟิสิกส์นิวเคลียร์',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/11695-2020-07-10-04-01-03"
    },
    {
        "subject": "physics",
        "grade": "M5",
        "topic": 'ธรรมชาติของคลื่นและชนิดของคลื่น',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/8783-2018-09-20-06-45-28"
    },
    {
        "subject": "physics",
        "grade": "M4",
        "topic": 'ธรรมชาติและการพัฒนาทางฟิสิกส์',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/10554-2019-08-28-02-06-08"
    },
    {
        "subject": "physics",
        "grade": "M6",
        "topic": 'คลื่นแม่เหล็กไฟฟ้า',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/11529-2020-05-01-03-02-13"
    },
    {
        "subject": "physics",
        "grade": "M5",
        "topic": 'การมองเห็นและแสงสี',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/9776-2019-02-21-06-15-23"
    },
    {
        "subject": "physics",
        "grade": "M4",
        "topic": 'แรงและเวกเตอร์ของแรง',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/10555-2019-08-28-02-14-09"
    },
    {
        "subject": "physics",
        "grade": "M5",
        "topic": 'ไฟฟ้ากระแส',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/11245-2019-12-19-07-35-22"
    },
    {
        "subject": "physics",
        "grade": "M4",
        "topic": 'การหมุน',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7318-2017-06-14-16-00-50"
    },
    {
        "subject": "physics",
        "grade": "M4",
        "topic": 'สภาพสมดุล และสภาพยืดหยุ่น',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7317-2017-06-14-15-58-37"
    },
    {
        "subject": "physics",
        "grade": "M5",
        "topic": 'แม่เหล็ก และไฟฟ้า (Magnets and Electricity)',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7886-2018-02-27-03-49-23"
    },
    {
        "subject": "physics",
        "grade": "M4",
        "topic": 'ระบบหน่วยระหว่างชาติ',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/8780-2018-09-20-06-42-49"
    },
    {
        "subject": "physics",
        "grade": "M6",
        "topic": 'สนามแม่เหล็ก',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7320-2017-06-14-16-05-39"
    },
    {
        "subject": "physics",
        "grade": "M6",
        "topic": 'ปรากกฎการณ์ของโลก',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7868-2018-02-26-08-27-01"
    },
    {
        "subject": "physics",
        "grade": "M6",
        "topic": 'ระบบสุริยะ และการกําเนิดระบบสุริยะ (Origin of Solar System)',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7316-origin-of-solar-system"
    },
    {
        "subject": "physics",
        "grade": "M4",
        "topic": 'โมเมนตัม การชน',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7313-2017-06-14-15-44-48"
    },
    {
        "subject": "physics",
        "grade": "M5",
        "topic": 'คลื่น',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7315-2017-06-14-15-51-22"
    },
    {
        "subject": "physics",
        "grade": "M5",
        "topic": 'ประจุไฟฟ้า',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7435-2017-08-11-04-18-55"
    },
    {
        "subject": "physics",
        "grade": "M4",
        "topic": 'แรงในธรรมชาติ 1',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7434-1-7434"
    },
    {
        "subject": "physics",
        "grade": "M4",
        "topic": 'การเคลื่อนที่ในแนวเส้นตรง',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7298-2017-06-14-15-00-03"
    },
    {
        "subject": "physics",
        "grade": "M4",
        "topic": 'การเคลื่อนที่แบบต่างๆ',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7299-2017-06-14-15-02-43"
    },
    {
        "subject": "physics",
        "grade": "M4",
        "topic": 'การเคลื่อนที่แบบหมุน',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7300-2017-06-14-15-05-53"
    },
    {
        "subject": "physics",
        "grade": "M6",
        "topic": 'แสงเป็นคลื่นหรืออนุภาค?',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7311-2017-06-14-15-35-21"
    },
    {
        "subject": "physics",
        "grade": "M6",
        "topic": 'พายุสุริยะ (solar storm): ปรากฎการณ์ทางฟิสิกส์',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7303-solar-storm"
    },
    {
        "subject": "physics",
        "grade": "M6",
        "topic": 'ดาวฤกษ์ (Star)',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7292-star"
    },
    {
        "subject": "physics",
        "grade": "M6",
        "topic": 'สึนามิ (Tsunami)',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7288-tsunami"
    },
    {
        "subject": "physics",
        "grade": "M6",
        "topic": 'เอกภพ (Universe)',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7293-universe-7293"
    },
    {
        "subject": "physics",
        "grade": "M6",
        "topic": 'แผ่นดินไหว (earthquake)',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7287-earthquake-earthquake"
    },
    {
        "subject": "physics",
        "grade": "M6",
        "topic": 'ทรายดูด (Quicksand)',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7281-quicksand"
    },
    {
        "subject": "physics",
        "grade": "M5",
        "topic": 'ปรากฏการณ์ดอปเพลอร์',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7279-2017-06-13-14-47-52"
    },
    {
        "subject": "physics",
        "grade": "M5",
        "topic": 'แสงสว่างกับการมองเห็น',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7277-2017-06-13-14-42-30"
    },
    {
        "subject": "physics",
        "grade": "M5",
        "topic": 'ไฟฟ้าและแม่เหล็ก',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7275-2017-06-13-14-37-07"
    },
    {
        "subject": "physics",
        "grade": "M5",
        "topic": 'การหักเหของแสง',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7282-2017-06-14-13-59-29"
    },
    {
        "subject": "physics",
        "grade": "M5",
        "topic": 'ภาพที่เกิดจากกระจกเงา',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7278-2017-06-13-14-46-38"
    },
    {
        "subject": "physics",
        "grade": "M5",
        "topic": 'หลอดไฟแอลอีดี (LED)',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7276-led"
    },
    {
        "subject": "physics",
        "grade": "M4",
        "topic": 'การวัดและหน่วยวัด',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7260-2017-06-12-16-08-32"
    },
    {
        "subject": "physics",
        "grade": "M6",
        "topic": 'ฟิสิกส์อะตอม',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7267-2017-06-13-14-06-26"
    },
    {
        "subject": "physics",
        "grade": "M6",
        "topic": 'ความรู้เกี่ยวกับ ของไหล (Fluid)',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7268-fluid"
    },
    {
        "subject": "physics",
        "grade": "M6",
        "topic": 'กัมมันตรังสี',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7265-2017-06-13-13-55-11"
    },
    {
        "subject": "physics",
        "grade": "M5",
        "topic": 'เสียงและมนุษย์',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7262-2017-06-13-13-37-52"
    },
    {
        "subject": "physics",
        "grade": "M6",
        "topic": 'ฟิสิกส์นิวเคลียร์',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7269-2017-06-13-14-13-42"
    },
    {
        "subject": "physics",
        "grade": "M6",
        "topic": 'รู้เรื่องพลังงานนิวเคลียร์',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7264-2017-06-13-13-47-06"
    },
    {
        "subject": "physics",
        "grade": "M5",
        "topic": 'การเคลื่อนที่แบบคลื่น',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7261-2017-06-12-16-09-47"
    },
    {
        "subject": "physics",
        "grade": "M4",
        "topic": 'การเคลื่อนที่ใน 1 และ 2 มิติ',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7266-1-2"
    },
    {
        "subject": "physics",
        "grade": "M5",
        "topic": 'เลเซอร์',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7263-2017-06-13-13-39-22"
    },
    {
        "subject": "physics",
        "grade": "M5",
        "topic": 'ความร้อน (heat)',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7250-heat"
    },
    {
        "subject": "physics",
        "grade": "M5",
        "topic": 'คลื่นเสียง',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7247-2017-06-12-15-31-26"
    },
    {
        "subject": "physics",
        "grade": "M4",
        "topic": 'แรงพื้นฐานในธรรมชาติ',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7249-fundamental-of-force"
    },
    {
        "subject": "physics",
        "grade": "M4",
        "topic": 'การจำแนกคลื่น',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7248-2017-06-12-15-38-24"
    },
    {
        "subject": "physics",
        "grade": "M6",
        "topic": 'พลังงานศักย์ไฟฟ้า ศักย์ไฟฟ้า และความจุไฟฟ้า',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7243-2017-06-12-15-11-30"
    },
    {
        "subject": "physics",
        "grade": "M5",
        "topic": 'แสงและเลนส์',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7245-2017-06-12-15-27-50"
    },
    {
        "subject": "physics",
        "grade": "M5",
        "topic": 'คลื่นกล',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7246-2017-06-12-15-29-38"
    },
    {
        "subject": "physics",
        "grade": "M5",
        "topic": 'แสงและกระจก',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7244-2017-06-12-15-21-13"
    },
    {
        "subject": "physics",
        "grade": "M4",
        "topic": 'สภาพสมดุล (Equilibrium)',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7226-equilibrium"
    },
    {
        "subject": "physics",
        "grade": "M6",
        "topic": 'สนามไฟฟ้า กฎของคูลอมบ์ และกฎของเกาส์',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7239-2017-06-11-14-21-08"
    },
    {
        "subject": "physics",
        "grade": "M6",
        "topic": 'กฎของฟาราเดย์',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7238-2017-06-11-14-17-45"
    },
    {
        "subject": "physics",
        "grade": "M5",
        "topic": 'ทฤษฎีเทอร์โมไดนามิกส์',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7240-2017-06-11-14-22-46"
    },
    {
        "subject": "physics",
        "grade": "M6",
        "topic": 'การประยุกต์ใช้กฎของเคอร์ชอฟฟ์ (Kirchhoff’s Law)',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7235-kirchhoff-s-law"
    },
    {
        "subject": "physics",
        "grade": "M6",
        "topic": 'สารกึ่งตัวนำ',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7237-2017-06-11-14-15-33"
    },
    {
        "subject": "physics",
        "grade": "M6",
        "topic": 'การประยุกต์ใช้กฎของโอหม์ (Ohm’s Law)',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7234-ohm-s-law"
    },
    {
        "subject": "physics",
        "grade": "M4",
        "topic": 'ฟิสิกส์ของนิวตัน',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7232-2017-06-11-13-39-43"
    },
    {
        "subject": "physics",
        "grade": "M5",
        "topic": 'ของไหล',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7227-2017-06-11-11-59-45"
    },
    {
        "subject": "physics",
        "grade": "M6",
        "topic": 'เทคนิคการวิเคราะห์วงจรด้วยวิธีโนด และวิธีลูป (เมช)',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7236-nodal-and-loop-mesh-analysis-technique"
    },
    {
        "subject": "physics",
        "grade": "M6",
        "topic": 'ทฤษฎีสัมพัทธภาพ',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7220-2017-06-11-05-36-38"
    },
    {
        "subject": "physics",
        "grade": "M5",
        "topic": 'คลื่นกล (Mechanical wave)',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7209-mechanical-wave-mechanical-wave"
    },
    {
        "subject": "physics",
        "grade": "M4",
        "topic": 'การชนและโมเมนตัมเชิงเส้น',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7221-2017-06-11-05-48-35"
    },
    {
        "subject": "physics",
        "grade": "M5",
        "topic": 'คลื่นนิ่งและการสั่นพ้อง',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7213-2017-06-11-04-00-08"
    },
    {
        "subject": "physics",
        "grade": "M5",
        "topic": 'คุณสมบัติของคลื่น (2)',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7212-2"
    },
    {
        "subject": "physics",
        "grade": "M5",
        "topic": 'เสียง (Sound)',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7214-sound"
    },
    {
        "subject": "physics",
        "grade": "M5",
        "topic": 'คุณสมบัติของคลื่น (1)',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7211-1"
    },
    {
        "subject": "physics",
        "grade": "M6",
        "topic": 'ฟิสิกส์อะตอม (Atomic Physics)',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7217-atomic-physics-atomic-physics"
    },
    {
        "subject": "physics",
        "grade": "M4",
        "topic": "Laws of Motion",
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7207-laws-of-motion"
    },
    {
        "subject": "physics",
        "grade": "M6",
        "topic": 'ไฟฟ้ากระแสตรง',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7216-2017-06-11-04-25-23"
    },
    {
        "subject": "physics",
        "grade": "M6",
        "topic": 'แม่เหล็กไฟฟ้า (Electromagnetics)',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7218-electromagnetics"
    },
    {
        "subject": "physics",
        "grade": "M6",
        "topic": 'ปรากฏการณ์ทางธรรมชาติของไฟฟ้า',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7206-2017-06-11-03-15-48"
    },
    {
        "subject": "physics",
        "grade": "M6",
        "topic": 'ตัวเก็บประจุ (Capacitor)',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7205-capacitor"
    },
    {
        "subject": "physics",
        "grade": "M4",
        "topic": 'หลักการคงตัวของโมเมนตัมเชิง...แมว',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7142-2017-06-04-08-55-10"
    },
    {
        "subject": "physics",
        "grade": "M5",
        "topic": 'เครื่องบิน บินได้อย่างไร',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7141-2017-06-04-08-52-24"
    },
    {
        "subject": "physics",
        "grade": "M5",
        "topic": 'เล่นกับจุดเดือด',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7144-2017-06-04-09-00-33"
    },
    {
        "subject": "physics",
        "grade": "M6",
        "topic": '115 ปี รังสีมหาประโยชน์',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7150-115"
    },
    {
        "subject": "physics",
        "grade": "M5",
        "topic": "Fluids",
        "scimath_url": "https://www.scimath.org/lesson-physics/item/7139-fluids"
    },
    {
        "subject": "physics",
        "grade": "M5",
        "topic": 'คลื่นกล (Mechanical wave)',
        "scimath_url": "https://www.scimath.org/lesson-physics/item/6975-mechanical-wave"
    },

    # Biology 115 Entries
    {
        "subject": "biology",
        "grade": "M6",
        "topic": 'ความหลากหลายทางชีวภาพ (Biodiversity)',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/11004-biodiversity"
    },
    {
        "subject": "biology",
        "grade": "M6",
        "topic": 'ทรัพยากรธรรมชาติ',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/11674-2020-06-30-07-32-32"
    },
    {
        "subject": "biology",
        "grade": "M5",
        "topic": 'อาณาจักรพืช',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/11307-2020-02-17-07-09-18"
    },
    {
        "subject": "biology",
        "grade": "M4",
        "topic": 'อาณาจักรมอเนอรา (Kingdom Monera)',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/11005-2019-10-29-01-49-12"
    },
    {
        "subject": "biology",
        "grade": "M5",
        "topic": 'พืชดอก',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/10518-2019-07-18-01-42-50"
    },
    {
        "subject": "biology",
        "grade": "M4",
        "topic": 'อาณาจักรโพรทิสตา',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/11306-2020-02-17-06-56-12"
    },
    {
        "subject": "biology",
        "grade": "M4",
        "topic": 'อาณาจักรสัตว์',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/11530-2020-05-01-03-04-18"
    },
    {
        "subject": "biology",
        "grade": "M4",
        "topic": 'อาณาจักรฟังไจ',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/11312-2020-02-18-04-05-10"
    },
    {
        "subject": "biology",
        "grade": "M4",
        "topic": 'เคมีที่เป็นพื้นฐานของสิ่งมีชีวิต',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/10559-2019-08-28-02-42-02"
    },
    {
        "subject": "biology",
        "grade": "M4",
        "topic": 'อาณาจักรไวรา',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/11673-2020-06-30-07-30-57"
    },
    {
        "subject": "biology",
        "grade": "M5",
        "topic": 'การสังเคราะห์แสงของพืช',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/10517-2019-07-18-01-41-56"
    },
    {
        "subject": "biology",
        "grade": "M5",
        "topic": 'การแลกเปลี่ยนแก๊สในสัตว์',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/10516-2019-07-18-01-40-45"
    },
    {
        "subject": "biology",
        "grade": "M6",
        "topic": 'ภาวะความสัมพันธ์ของสิ่งมีชีวิตในสิ่งแวดล้อม',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/9796-2019-02-21-07-11-20"
    },
    {
        "subject": "biology",
        "grade": "M6",
        "topic": 'การถ่ายทอดพลังงานในระบบนิเวศ',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/9642-2018-12-14-08-29-47"
    },
    {
        "subject": "biology",
        "grade": "M5",
        "topic": 'สิ่งเร้าที่มีผลต่อพืช',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/9432-2018-11-14-08-51-04"
    },
    {
        "subject": "biology",
        "grade": "M4",
        "topic": 'เซลล์ สิ่งมีชีวิตขนาดเล็ก',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/10323-2019-05-13-06-01-55"
    },
    {
        "subject": "biology",
        "grade": "M4",
        "topic": 'เชื้อรา',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/9637-1-9637"
    },
    {
        "subject": "biology",
        "grade": "M4",
        "topic": 'ความหลากหลายของสัตว์',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/9434-2018-11-14-08-52-40"
    },
    {
        "subject": "biology",
        "grade": "M4",
        "topic": 'รู้ทันแบคทีเรีย',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/9795-2019-02-21-07-08-54"
    },
    {
        "subject": "biology",
        "grade": "M5",
        "topic": 'ประวัติศาสตร์ทางพันธุกรรม',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/9429-2018-11-14-08-47-17"
    },
    {
        "subject": "biology",
        "grade": "M6",
        "topic": 'ความสัมพันธ์ของระบบนิเวศ',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/10322-2019-05-13-06-00-45"
    },
    {
        "subject": "biology",
        "grade": "M4",
        "topic": 'สัตว์ปีกน่ารู้',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/9794-2019-02-21-07-00-57"
    },
    {
        "subject": "biology",
        "grade": "M4",
        "topic": 'สิ่งมีชีวิตเซลล์เดียว',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/9433-2018-11-14-08-51-53"
    },
    {
        "subject": "biology",
        "grade": "M4",
        "topic": 'กล้องจุลทรรศน์ และส่วนประกอบของกล้องจุลทรรศน์',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7873-2018-02-27-02-46-18"
    },
    {
        "subject": "biology",
        "grade": "M6",
        "topic": 'หมู่โลหิต',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/8802-2018-09-21-02-18-35"
    },
    {
        "subject": "biology",
        "grade": "M5",
        "topic": 'การรักษาดุลยภาพ',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7874-2018-02-27-03-05-55"
    },
    {
        "subject": "biology",
        "grade": "M6",
        "topic": 'จีโนม',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/8801-2018-09-21-02-13-37"
    },
    {
        "subject": "biology",
        "grade": "M6",
        "topic": 'พืช GMO',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/8800-gmo"
    },
    {
        "subject": "biology",
        "grade": "M5",
        "topic": 'เนื้อเยื่อพืช',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7875-2018-02-27-03-09-55"
    },
    {
        "subject": "biology",
        "grade": "M4",
        "topic": 'การเก็บรักษาเชื้อบริสุทธิ์',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7449-2017-08-11-07-35-19"
    },
    {
        "subject": "biology",
        "grade": "M4",
        "topic": 'การแยกเชื้อบริสุทธิ์',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7448-2017-08-11-07-30-49"
    },
    {
        "subject": "biology",
        "grade": "M4",
        "topic": 'การหายใจระดับเซลล์',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7440-2017-08-11-04-44-12"
    },
    {
        "subject": "biology",
        "grade": "M4",
        "topic": 'ชีววิทยาของเซลล์: ส่วนประกอบของเซลล์ การลําเลียงสารของเซลล์',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7450-2017-08-11-07-37-33"
    },
    {
        "subject": "biology",
        "grade": "M6",
        "topic": 'เด็กหลอดแก้ว',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/8799-2018-09-21-02-10-48"
    },
    {
        "subject": "biology",
        "grade": "M6",
        "topic": 'ยีนและการแสดงออกของยีน',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7132-2017-06-04-08-01-40"
    },
    {
        "subject": "biology",
        "grade": "M5",
        "topic": 'การสืบพันธุ์ของสิ่งมีชีวิต',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7056-2017-05-23-14-43-19"
    },
    {
        "subject": "biology",
        "grade": "M6",
        "topic": 'ลักษณะการเรียงตัวของ DNA ในจีโนม',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7133-dna-7133"
    },
    {
        "subject": "biology",
        "grade": "M5",
        "topic": 'ทำไมกระเพาะอาหารจึงไม่ย่อยตัวเอง?',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7128-2017-06-04-07-52-38"
    },
    {
        "subject": "biology",
        "grade": "M5",
        "topic": 'ระบบต่อมไร้ท่อ (endocrine system)',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7123-2017-06-04-07-31-16"
    },
    {
        "subject": "biology",
        "grade": "M6",
        "topic": 'ความหลากหลายทางชีวภาพ',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7055-2017-05-23-14-39-52"
    },
    {
        "subject": "biology",
        "grade": "M4",
        "topic": 'ชีววิทยาของเซลล์ (cell biology)',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7054-cell-biology"
    },
    {
        "subject": "biology",
        "grade": "M6",
        "topic": 'สิ่งมีชีวิตกับดีเอ็นเอ',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7131-2017-06-04-07-58-25"
    },
    {
        "subject": "biology",
        "grade": "M6",
        "topic": 'ภูมิปัญญาชาวบ้านกับความหลากหลายทางชีวภาพ',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7051-2017-05-23-14-19-46"
    },
    {
        "subject": "biology",
        "grade": "M5",
        "topic": 'การเคลื่อนที่ของโปรติสตาเเละสัตว์',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7046-2017-05-22-15-26-07"
    },
    {
        "subject": "biology",
        "grade": "M4",
        "topic": 'เคมีที่เป็นพื้นฐานของสิ่งมีชีวิต',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7053-2017-05-23-14-26-12"
    },
    {
        "subject": "biology",
        "grade": "M4",
        "topic": 'จุลชีววิทยา (Microbiology)',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7047-microbiology"
    },
    {
        "subject": "biology",
        "grade": "M6",
        "topic": "Descent with modification",
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7049-descent-with-modification"
    },
    {
        "subject": "biology",
        "grade": "M6",
        "topic": 'พฤติกรรมสัตว์ (Animal Behavior)',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7042-animal-behavior"
    },
    {
        "subject": "biology",
        "grade": "M4",
        "topic": 'การหายใจระดับเซลล์',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7045-2017-05-22-15-22-23"
    },
    {
        "subject": "biology",
        "grade": "M5",
        "topic": 'ระบบต่าง ๆ ของร่างกาย',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7044-2017-05-22-15-19-05"
    },
    {
        "subject": "biology",
        "grade": "M5",
        "topic": 'ระบบประสาท (nervous system)',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7048-nervous-system"
    },
    {
        "subject": "biology",
        "grade": "M4",
        "topic": 'อาณาจักรของสิ่งมีชีวิต',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7043-2017-05-22-15-05-34"
    },
    {
        "subject": "biology",
        "grade": "M4",
        "topic": 'การลำเลียงสาร',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7050-2017-05-23-14-01-13"
    },
    {
        "subject": "biology",
        "grade": "M5",
        "topic": 'การสังเคราะห์อาหารด้วยเเสง (photosynthesis)',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7052-photosynthesis-7052"
    },
    {
        "subject": "biology",
        "grade": "M4",
        "topic": 'การสลายสารอาหารระดับเซลล์ (Cellular respiration)',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7029-cellular-respiration-7029"
    },
    {
        "subject": "biology",
        "grade": "M4",
        "topic": 'วิทยาศาสตร์เเละชีววิทยา',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7041-2017-05-22-14-56-59"
    },
    {
        "subject": "biology",
        "grade": "M5",
        "topic": 'ระบบภูมิคุ้มกัน (Immunology)',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7030-immunology"
    },
    {
        "subject": "biology",
        "grade": "M5",
        "topic": 'ทำไมเราถึงป่วย',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7032-2017-05-21-15-05-29"
    },
    {
        "subject": "biology",
        "grade": "M5",
        "topic": 'โครงสร้างพืช (plant structure)',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7039-plant-structure"
    },
    {
        "subject": "biology",
        "grade": "M5",
        "topic": 'ระบบย่อยอาหาร (digestive system)',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7036-digestive-system-7036"
    },
    {
        "subject": "biology",
        "grade": "M4",
        "topic": "Animal Kingdom - Invertebrate",
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7035-animal-kingdom-invertebrate"
    },
    {
        "subject": "biology",
        "grade": "M4",
        "topic": 'ชีววิทยาสำหรับนักเรียนมัธยมศึกษาตอนต้น',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7034-2017-05-21-15-16-43"
    },
    {
        "subject": "biology",
        "grade": "M6",
        "topic": 'นิเวศวิทยา',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7040-2017-05-22-14-49-08"
    },
    {
        "subject": "biology",
        "grade": "M5",
        "topic": 'โครงสร้างและหน้าที่ของพืชดอก (Plant form and function)',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7031-plant-form-and-function"
    },
    {
        "subject": "biology",
        "grade": "M5",
        "topic": 'ฮอร์โมนคือ (Hormone)',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7038-hormone-7038"
    },
    {
        "subject": "biology",
        "grade": "M4",
        "topic": 'วิตามินเเละโคเอนไซม์',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7033-2017-05-21-15-14-03"
    },
    {
        "subject": "biology",
        "grade": "M5",
        "topic": 'ระบบภูมิคุ้มกันในร่างกาย',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7027-2017-05-21-08-44-33"
    },
    {
        "subject": "biology",
        "grade": "M6",
        "topic": 'อนาคตของเรา ยาที่ตรงกับพันธุกรรม',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7021-2017-05-21-07-14-40"
    },
    {
        "subject": "biology",
        "grade": "M6",
        "topic": "Ecology",
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7015-ecology"
    },
    {
        "subject": "biology",
        "grade": "M5",
        "topic": 'ระบบประสาท',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7016-2017-05-21-05-11-43"
    },
    {
        "subject": "biology",
        "grade": "M6",
        "topic": 'ระบบนิเวศ',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7028-2017-05-21-14-25-17"
    },
    {
        "subject": "biology",
        "grade": "M5",
        "topic": 'ฮอร์โมน (Hormone)',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7020-hormone"
    },
    {
        "subject": "biology",
        "grade": "M6",
        "topic": 'เครื่องหมายดีเอ็นเอ',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7022-2017-05-21-07-28-11"
    },
    {
        "subject": "biology",
        "grade": "M5",
        "topic": "Metamorphosis",
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7018-metamorphosis"
    },
    {
        "subject": "biology",
        "grade": "M4",
        "topic": 'กล้องจุลทรรศน์',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7017-2017-05-21-05-20-05"
    },
    {
        "subject": "biology",
        "grade": "M5",
        "topic": 'การเคลื่อนที่ของสิ่งมีชีวิต',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7025-2017-05-21-08-09-47"
    },
    {
        "subject": "biology",
        "grade": "M5",
        "topic": 'โครงสร้างพืช',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7019-2017-05-21-06-56-10"
    },
    {
        "subject": "biology",
        "grade": "M4",
        "topic": 'การศึกษาสิ่งมีชีวิต',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7026-2017-05-21-08-12-50"
    },
    {
        "subject": "biology",
        "grade": "M4",
        "topic": "Carbohydrate",
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7009-carbohydrate"
    },
    {
        "subject": "biology",
        "grade": "M4",
        "topic": "Protein",
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7010-protein"
    },
    {
        "subject": "biology",
        "grade": "M6",
        "topic": 'ความผิดปกติของโครโมโซม',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7008-2017-05-21-04-16-59"
    },
    {
        "subject": "biology",
        "grade": "M4",
        "topic": "Lipid",
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7012-lipid"
    },
    {
        "subject": "biology",
        "grade": "M5",
        "topic": 'ระบบโครงร่างและการเคลื่อนไหว',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7005-2017-05-17-15-18-32"
    },
    {
        "subject": "biology",
        "grade": "M4",
        "topic": 'เคมีพื้นฐานของสิ่งมีชีวิต',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7002-2017-05-17-14-36-18"
    },
    {
        "subject": "biology",
        "grade": "M6",
        "topic": 'การนำความรู้ทางพันธุศาสตร์มาประยุกต์ใช้กับทางกฎหมาย',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7004-2017-05-17-14-56-25"
    },
    {
        "subject": "biology",
        "grade": "M4",
        "topic": "cell cycle, cell growth, and differentiation cell cycle, cell growth, and differentiation",
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7007-cell-cycle-cell-growth-and-differentiation-cell-cycle-cell-growth-and-differentiation"
    },
    {
        "subject": "biology",
        "grade": "M6",
        "topic": 'แมลง สิ่งมีชีวิตที่มีการแพร่กระจายบนโลกนี้มากที่สุด',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7006-2017-05-21-03-59-14"
    },
    {
        "subject": "biology",
        "grade": "M6",
        "topic": 'พฤติกรรม (Behavior)',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7001-behavior-7001"
    },
    {
        "subject": "biology",
        "grade": "M5",
        "topic": 'ฮอร์โมนพืช (phytohormone)',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7014-phytohormone"
    },
    {
        "subject": "biology",
        "grade": "M5",
        "topic": 'ผลไม้',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7013-2017-05-21-04-37-00"
    },
    {
        "subject": "biology",
        "grade": "M4",
        "topic": 'เอนไซม์และการทำงานของเอนไซม์',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/6998-2017-05-17-14-06-15"
    },
    {
        "subject": "biology",
        "grade": "M4",
        "topic": 'ทำไมถึงเป็นสิ่งมีชีวิต',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/6990-2017-05-16-14-51-04"
    },
    {
        "subject": "biology",
        "grade": "M5",
        "topic": 'การสืบพันธุ์และการเจริญเติบโต',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/6992-2017-05-16-15-02-46"
    },
    {
        "subject": "biology",
        "grade": "M5",
        "topic": "Photosynthesis",
        "scimath_url": "https://www.scimath.org/lesson-biology/item/6984-photosynthesis"
    },
    {
        "subject": "biology",
        "grade": "M6",
        "topic": 'ศิลปะแห่งสงครามแบคทีเรีย (the art of bacterial warfare)',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/6983-the-art-of-bacterial-warfare"
    },
    {
        "subject": "biology",
        "grade": "M5",
        "topic": 'การรักษาสมดุลของร่างกาย (Homeostasis)',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/6985-homeostasis"
    },
    {
        "subject": "biology",
        "grade": "M6",
        "topic": 'ความหลากหลายทางชีวภาพ (biodiversity)',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/6989-biodiversity-6989"
    },
    {
        "subject": "biology",
        "grade": "M6",
        "topic": "Central dogma",
        "scimath_url": "https://www.scimath.org/lesson-biology/item/6987-central-dogma"
    },
    {
        "subject": "biology",
        "grade": "M4",
        "topic": 'กลูโคส พลังงานที่สมองใช้ได้และปลอดภัยเพียงอย่างเดัยว',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/7000-2017-05-17-14-21-09"
    },
    {
        "subject": "biology",
        "grade": "M5",
        "topic": 'ระบบขับถ่าย (Excretory System)',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/6993-excretory-system"
    },
    {
        "subject": "biology",
        "grade": "M6",
        "topic": 'ระบบการจัดกลุ่มของสิ่งมีชีวิตที่ได้รับการเชื่อถือมากที่สุดในปัจจุบัน',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/6994-2017-05-16-15-14-31"
    },
    {
        "subject": "biology",
        "grade": "M6",
        "topic": 'การถ่ายทอดทางพันธุกรรม',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/6997-2017-05-17-13-58-37"
    },
    {
        "subject": "biology",
        "grade": "M5",
        "topic": 'การจำแนกเพศพืช',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/6948-2017-05-15-14-12-38"
    },
    {
        "subject": "biology",
        "grade": "M5",
        "topic": "cellular respiration",
        "scimath_url": "https://www.scimath.org/lesson-biology/item/6980-cellular-respiration"
    },
    {
        "subject": "biology",
        "grade": "M4",
        "topic": 'สารเคมีในเซลล์สิ่งมีชีวิต',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/6982-2017-05-16-13-22-26"
    },
    {
        "subject": "biology",
        "grade": "M5",
        "topic": 'อายุเม็ดเลือด',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/6967-2017-05-15-15-53-37"
    },
    {
        "subject": "biology",
        "grade": "M4",
        "topic": "Double life of ATP",
        "scimath_url": "https://www.scimath.org/lesson-biology/item/6958-double-life-of-atp"
    },
    {
        "subject": "biology",
        "grade": "M4",
        "topic": 'การขนส่งสารผ่านเยื่อหุ้มเซลล์ (membrane transport)',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/6976-membrane-transport"
    },
    {
        "subject": "biology",
        "grade": "M6",
        "topic": "Behavior",
        "scimath_url": "https://www.scimath.org/lesson-biology/item/6981-behavior"
    },
    {
        "subject": "biology",
        "grade": "M5",
        "topic": 'ระบบการแลกเปลี่ยนแก๊ส (Respiratory System)',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/6977-respiratory-system"
    },
    {
        "subject": "biology",
        "grade": "M4",
        "topic": 'โครงสร้างและหน้าที่ของเซลล์',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/6937-2017-05-15-13-01-38"
    },
    {
        "subject": "biology",
        "grade": "M5",
        "topic": 'สิ่งมีชีวิตที่สามารถสังเคราะห์เเสงได้',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/6962-2017-05-15-15-39-21"
    },
    {
        "subject": "biology",
        "grade": "M5",
        "topic": "plantae kingdom",
        "scimath_url": "https://www.scimath.org/lesson-biology/item/6979-plantae-kingdom"
    },
    {
        "subject": "biology",
        "grade": "M6",
        "topic": 'ต่างกันเพียง 1%',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/6964-1"
    },
    {
        "subject": "biology",
        "grade": "M6",
        "topic": 'โครโมโซม',
        "scimath_url": "https://www.scimath.org/lesson-biology/item/6894-2017-05-14-03-59-30"
    }
]

# Subject and grade display metadata
SUBJECT_META = {
    "math": {"display": "Mathematics", "display_th": "คณิตศาสตร์", "icon": "math", "color": "#4F46E5"},
    "chemistry": {"display": "Chemistry", "display_th": "เคมี", "icon": "chemistry", "color": "#0891B2"},
    "physics": {"display": "Physics", "display_th": "ฟิสิกส์", "icon": "physics", "color": "#7C3AED"},
    "biology": {"display": "Biology", "display_th": "ชีววิทยา", "icon": "biology", "color": "#059669"},
}

GRADE_META = {
    "M4": {"display": "Mathayom 4 (Grade 10)", "display_th": "ม.4"},
    "M5": {"display": "Mathayom 5 (Grade 11)", "display_th": "ม.5"},
    "M6": {"display": "Mathayom 6 (Grade 12)", "display_th": "ม.6"},
}
