# 🔧 Easy Project Configuration & Rebranding

**Want to remove personal references or customize the system for your company? Here's how:**

## 🚀 Quick Fix: Remove Personal Names

### Option 1: One Command Solution
```bash
# Download and run the rebranding script
python rebrand_project.py --preset generic

# This automatically changes:
# ✅ "Sergio Sebastian" → "System Developer" 
# ✅ "Daniel Uslenghi" → "Technical Expert"
# ✅ "Multipoint S.A." → "Your Company"
# ✅ All email and contact references
```

### Option 2: Environment Variables (Easiest)
```bash
# In your .env file:
PROJECT_NAME=My HVAC System
COMPANY_NAME=My Company
DEVELOPER_NAME=My Development Team
DEVELOPER_EMAIL=support@mycompany.com
END_USER_NAME=Technical Manager
SYSTEM_TITLE=My HVAC Support AI
HVAC_BRAND=Generic HVAC
```

### Option 3: Direct Configuration
Edit `config/project_config.py`:
```python
@dataclass
class ProjectConfig:
    company_name: str = "Your Company Name"
    developer_name: str = "Your Development Team" 
    developer_email: str = "support@yourcompany.com"
    end_user_name: str = "Technical Manager"
    hvac_brand: str = "Multi-Brand HVAC"
```

## 🎨 Available Presets

### Generic (Removes all personal info)
```bash
python rebrand_project.py --preset generic
```

### Enterprise
```bash
python rebrand_project.py --preset enterprise  
```

### Custom
Create your own preset in the config file.

## 🛡️ Safety Features

- **🔄 Automatic Backup**: Creates backup before any changes
- **👁️ Preview Mode**: See what would change: `--preview`
- **🔧 Easy Restore**: All backups saved in `backup_before_rebrand/`

## 📁 What Gets Updated

The system automatically updates ALL references across:
- README files and documentation
- Source code comments and strings
- Configuration files
- API descriptions
- System branding

## 🚀 After Rebranding

```bash
# 1. Test the system
python launch_ultimate_graphrag.py --mode demo

# 2. Update your credentials  
cp .env.example .env
# Edit .env with your Neo4j and OpenAI keys

# 3. Launch production API
python launch_ultimate_graphrag.py --mode api
```

---

**The system is designed to be easily white-labeled and customized for any company or use case!** 🎯

For detailed instructions, see `CONFIGURATION_GUIDE.md` after cloning the repository.
