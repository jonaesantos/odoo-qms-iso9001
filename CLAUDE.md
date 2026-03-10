# Claude Instructions for TMC Odoo Module

## Project Overview

This is the TMC (Tribunal Municipal de Cuentas de Rosario) module for Odoo 19.0, providing a Document Management System (Sistema de Gestión Documental).

## Commit Message Style

Follow this repository's commit message conventions and the official Odoo Git Guidelines:
**Reference**: https://www.odoo.com/documentation/19.0/contributing/development/git_guidelines.html

### Format

```
[TYPE] Brief description

- Detailed change 1
- Detailed change 2
- Detailed change 3
```

### Commit Types

- `[IMP]` - Improvements and enhancements
- `[FIX]` - Bug fixes
- `[ADD]` - Add new features or modules
- `[REM]` - Remove features or code
- `[REF]` - Refactoring (no functional changes)
- `[MIG]` - Migration between Odoo versions
- `[UPD]` - Updates to documentation or configurations
- `[WIP]` - Work in progress (avoid in main branch)

### Guidelines

- **Follow Odoo's official guidelines** at the link above for detailed commit structure
- Use imperative mood ("Add feature" not "Added feature")
- Focus on "why" rather than just "what"
- Keep the first line concise and descriptive (ideally under 72 characters)
- Use bullet points for detailed changes
- Reference issue/ticket numbers when applicable
- **DO NOT include AI attribution** (no "Generated with Claude Code" or "Co-Authored-By: Claude")
- One logical change per commit (split unrelated changes into separate commits)

### Examples

```
[ADD] Initial module structure for document tracking

- Created document model with basic fields
- Added security rules and access rights
- Implemented basic views (form, list, search)
```

```
[IMP] Enhanced document workflow

- Added state management for document processing
- Improved form view layout for better UX
- Added computed fields for document statistics
```

```
[FIX] Compute method for document metrics

- Fixed domain filter in related document lines
- Added proper aggregation handling
- Ensured compute triggers on all dependencies
```

## Environment and Dependencies

- **Python Version:** 3.12
- **Odoo Version:** 19.0
- **ORM:** Odoo ORM
- **Web Framework:** Odoo Web (OWL)
- **Testing Framework:** Odoo's built-in testing tools (unittest)
- **Code Linting:** pylint-odoo
- **XML/Views Validation:** Odoo's QWeb validation

## Recommended Module Structure

```text
my_module/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── my_model.py
├── views/
│   └── my_model_views.xml
├── controllers/
│   ├── __init__.py
│   └── my_controller.py
├── security/
│   ├── ir.model.access.csv
│   └── security.xml
├── data/
│   └── data_file.xml
├── static/
│   ├── description/
│   │   ├── icon.png
│   │   └── index.html
│   └── src/
│       ├── js/
│       ├── css/
│       └── xml/
├── report/
│   └── my_report.xml
├── i18n/
│   ├── es.po
│   └── en.po
└── tests/
    ├── __init__.py
    └── test_my_module.py
```

## Best Practices

### 1. Modeling and Validation

- Use Odoo ORM for all model definitions
- Define constraints using `_sql_constraints` for database-level constraints
- Use Python constraints (`@api.constrains`) for complex business logic validation
- Always validate user input before processing
- Use appropriate field types and avoid generic fields when specific ones exist

**Example:**

```python
class Dependence(models.Model):
    _name = 'tmc.dependence'
    _description = 'Dependence'

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', _('Dependence name must be unique'))
    ]

    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        for record in self:
            if record.date_end < record.date_start:
                raise ValidationError(_('End date must be after start date'))
```

### 2. Controllers and Routing

- Use Odoo's HTTP controllers for custom routes
- Protect routes with proper authentication decorators (`@http.route(..., auth='user')`)
- Return proper HTTP responses with appropriate status codes
- Use JSON for API endpoints

### 3. Views and UI

- Follow Odoo's QWeb standards for all views
- Use appropriate view types: `kanban`, `form`, `list`, `search`, `pivot`, `graph`
- Implement search views with proper filters, group_by, and domain
- Use field widgets appropriately (`many2many_tags`, `statusbar`, `monetary`, etc.)
- Keep views clean and organized with proper grouping and notebook pages

### 4. Security

- Always define access rights in `ir.model.access.csv` for every model
- Use record rules (`ir.rule`) for row-level security
- Follow the principle of least privilege
- Test security with different user roles

**Example ir.model.access.csv:**

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_my_model_user,my.model.user,model_my_model,base.group_user,1,0,0,0
access_my_model_manager,my.model.manager,model_my_model,base.group_system,1,1,1,1
```

### 5. Business Logic

- Keep all business logic inside the `models` directory
- Use computed fields (`@api.depends`) for derived data
- Use onchange methods (`@api.onchange`) for real-time form updates
- Override CRUD methods (`create`, `write`, `unlink`) when needed for business rules
- Use action methods for complex operations triggered by buttons

**Example:**

```python
@api.depends('document_topic_ids')
def _compute_document_topic_names(self):
    for record in self:
        record.document_topic_names = ", ".join(
            record.document_topic_ids.mapped('name')
        )

@api.depends('main_topic_ids')
def _compute_topics_display_name(self):
    for record in self:
        if record.main_topic_ids:
            record.topics_display_name = ", ".join(
                record.main_topic_ids.mapped('name')
            )
```

### 6. Performance Optimization

- Use Odoo's prefetching mechanism (avoid disabling it)
- Use `read_group` for aggregated queries
- Avoid N+1 queries by using `prefetch_fields` or eager loading
- Use `search_count()` instead of `len(search())`
- Batch operations when processing multiple records
- Use SQL queries sparingly and only when ORM is insufficient

**Example:**

```python
# Bad - N+1 queries
for document in documents:
    topics = document.main_topic_ids.mapped('name')

# Good - Prefetch
documents_with_topics = documents.with_prefetch(['main_topic_ids'])
for document in documents_with_topics:
    topics = document.main_topic_ids.mapped('name')

# Better - Use read_group for aggregation
topic_counts = self.env['tmc.document'].read_group(
    [('period', '=', '2025')],
    ['main_topic_ids'],
    ['main_topic_ids']
)
```

### 7. Module Manifest

- Complete the `__manifest__.py` with accurate metadata
- Specify all dependencies in the `depends` list
- Use semantic versioning
- Include proper `category`, `author`, `website`, and `license`
- List data files in correct load order

**Example:**

```python
{
    'name': 'TMC Base',
    'version': '19.0.1.0.0',
    'category': 'Document Management',
    'summary': 'Main TMC models and functionality',
    'description': """
        Document Management System for Tribunal Municipal de Cuentas
        Manages documents, dependencies, topics, and institutional classifiers
    """,
    'author': 'Tribunal Municipal de Cuentas - Municipalidad de Rosario',
    'website': 'https://www.tmcrosario.gob.ar',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'web_tree_many2one_clickable',
        'remove_odoo_enterprise',
    ],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/tmc_menus.xml',
        'views/document_views.xml',
        'views/document_menus.xml',
        'views/dependence_views.xml',
        'views/dependence_menus.xml',
    ],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}
```

### 8. Error Handling

- Use `UserError` for user-facing errors that users can fix
- Use `ValidationError` for validation failures
- Use `AccessError` for permission-related errors
- Provide clear, actionable error messages
- Always translate error messages with `_()`

**Example:**

```python
from odoo.exceptions import UserError, ValidationError

# From tmc.institutional_classifier
if year > datetime.today():
    raise UserError(_('Invalid period'))

if newest and values['period'] < newest[0].period:
    raise UserError(_('There is already a more recent nomenclator'))

# Validation example
if record.date_end < record.date_start:
    raise ValidationError(_('End date must be after start date'))
```

### 9. Code Style

- Follow Odoo's coding guidelines: https://www.odoo.com/documentation/19.0/contributing/development/coding_guidelines.html
- Use `pylint-odoo` for linting and code consistency
- Use meaningful variable and method names
- Keep methods short and focused (Single Responsibility Principle)
- Use proper Python conventions (PEP 8)
- Add blank lines between methods
- Group imports properly: standard library, third-party, Odoo imports

### 10. Internationalization

- Use `_()` for all translatable strings
- Generate `.pot` files with `odoo-bin --i18n-export`
- Include `.po` files for supported languages in `i18n/` directory
- Avoid string concatenation; use format strings or f-strings
- Keep strings simple and context-aware

### 11. Data Management

- Store initial data in the `data/` directory using XML or CSV formats
- Use `noupdate="1"` for data that should not be updated during module upgrades
- Use `noupdate="0"` (default) for data that should be updated
- Reference records using XML IDs
- Keep demo data separate in the `demo/` directory

### 12. Testing

- Write unit tests using Odoo's built-in testing framework
- Test business logic, computed fields, and constraints
- Test access rights with different user roles
- Use `TransactionCase` for most tests
- Use `HttpCase` for testing controllers
- Place tests in the `tests/` directory

**Example:**

```python
from odoo.tests import TransactionCase
from odoo.exceptions import ValidationError

class TestMyModel(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Model = self.env['my.model']

    def test_date_constraint(self):
        with self.assertRaises(ValidationError):
            self.Model.create({
                'date_start': '2025-01-01',
                'date_end': '2024-12-31',
            })
```

### 13. Module Upgrades

- Handle schema changes with migration scripts in `migrations/19.0.1.0.1/`
- Use `pre-` and `post-` migration scripts when needed
- Test upgrades on a copy of production data
- Document upgrade procedures for breaking changes

### 14. Documentation

- Include module documentation in a `README.rst` or `README.md` file
- Use docstrings for all classes and complex methods
- Document public API methods
- Include usage examples in documentation
- Keep the `static/description/index.html` up to date

### 15. Version Control

- Follow semantic versioning: `19.0.MAJOR.MINOR.PATCH`
- Version format: `{ODOO_VERSION}.{MAJOR}.{MINOR}.{PATCH}`
- Increment MAJOR for breaking changes
- Increment MINOR for new features
- Increment PATCH for bug fixes

### 16. Static Content

- Place images, JS, and CSS in the `static/` directory
- Follow Odoo's asset bundle system for JS/CSS
- Use appropriate asset bundles (`web.assets_backend`, `web.assets_frontend`)
- Minify static assets for production

### 17. Frontend Development (OWL)

- Use OWL (Odoo Web Library) for custom frontend components
- Follow Odoo's guidelines for QWeb templates
- Use proper component lifecycle hooks
- Handle state management properly
- Use Odoo's standard widgets when possible

### 18. Model Inheritance

- Prefer extending models using `_inherit` over copying code
- Use `_name` + `_inherit` for creating new models with inherited functionality
- Use delegation inheritance (`_inherits`) for composition patterns
- Never modify core Odoo code directly

**Example:**

```python
# Extension
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    custom_field = fields.Char('Custom Field')

# Delegation
class Document(models.Model):
    _name = 'tmc.document.custom'
    _inherits = {'tmc.document': 'document_id'}

    document_id = fields.Many2one('tmc.document', required=True, ondelete='cascade')
```

### 19. Configuration Management

- Use system parameters (`ir.config_parameter`) for configurable values
- Use `res.config.settings` for user-configurable options
- Avoid hardcoding values
- Provide sensible defaults

### 20. Code Comments

- Use comments sparingly and only for complex or non-obvious logic
- Prefer self-documenting code with clear names
- Use docstrings for public methods
- Explain "why" not "what" in comments

## Development Workflow

### When Making Changes

1. Create a new branch for each feature/fix
2. Update module version in `__manifest__.py` if needed
3. Run the module with `--dev=reload,xml,qweb` for faster iteration
4. Test changes thoroughly before committing
5. Run pylint-odoo on modified files
6. Update documentation if needed

## Common Patterns

### Wizard Pattern

Create transient models for wizards:

```python
class MassEditDocumentTopics(models.TransientModel):
    _name = 'tmc.mass_edit_document_topics_wizard'
    _description = 'Mass Edit Document Topics'

    main_topic_ids = fields.Many2many(
        comodel_name='tmc.document_topic',
        domain="[('parent_id', '=', False)]",
    )

    secondary_topic_ids = fields.Many2many(
        comodel_name='tmc.document_topic',
        domain="[('parent_id', 'in', main_topic_ids)]",
    )

    def save_document_topics(self):
        active_ids = self.env.context.get('active_ids', [])
        for document_id in active_ids:
            document_obj = self.env['tmc.document'].browse(document_id)
            document_obj.main_topic_ids |= self.main_topic_ids
            document_obj.secondary_topic_ids |= self.secondary_topic_ids
        return {'type': 'ir.actions.act_window_close'}
```

### Server Actions

Define server actions in XML for button actions:

```xml
<record id="action_server_my_action" model="ir.actions.server">
    <field name="name">My Action</field>
    <field name="model_id" ref="model_my_model"/>
    <field name="state">code</field>
    <field name="code">
        action = records.action_my_method()
    </field>
</record>
```

### Scheduled Actions (Cron)

```xml
<record id="ir_cron_my_task" model="ir.cron">
    <field name="name">My Scheduled Task</field>
    <field name="model_id" ref="model_my_model"/>
    <field name="state">code</field>
    <field name="code">model._cron_my_task()</field>
    <field name="interval_number">1</field>
    <field name="interval_type">days</field>
    <field name="numbercall">-1</field>
</record>
```

## References

- **Odoo 19.0 Documentation:** https://www.odoo.com/documentation/19.0/
- **Odoo Git Guidelines:** https://www.odoo.com/documentation/19.0/contributing/development/git_guidelines.html
- **Odoo Coding Guidelines:** https://www.odoo.com/documentation/19.0/contributing/development/coding_guidelines.html
- **OWL Documentation:** https://www.odoo.com/documentation/19.0/developer/reference/frontend/owl_components.html
- **Python PEP 8:** https://peps.python.org/pep-0008/

## TMC Module Structure

The TMC module consists of the following core models and functionality:

### Core Models

#### 1. `tmc.document`

The main document model that tracks all documents in the system.

**Key Fields:**

- `name` - Computed document name
- `dependence_id` - Related organizational unit (Many2one to `tmc.dependence`)
- `document_type_id` - Type of document (Many2one to `tmc.document_type`)
- `number` - Document number
- `period` - Year period (Selection field)
- `date` - Document date
- `document_object` - Brief description of document purpose
- `main_topic_ids` - Main topics (Many2many to `tmc.document_topic`)
- `secondary_topic_ids` - Secondary topics (Many2many to `tmc.document_topic`)
- `highlight_ids` - Document highlights/priorities (One2many to `tmc.highlight`)
- `important` - Boolean flag for important documents

**Key Features:**

- Period-based document tracking (year selection)
- Topic categorization with main and secondary topics
- Computed display names and topic summaries
- Document highlights for priority management
- References to related documents (dictamen relationships)

#### 2. `tmc.dependence`

Organizational units or dependencies within the municipality.

**Key Fields:**

- `name` - Dependence name (unique)
- `abbreviation` - Short code for the dependence
- `document_type_ids` - Allowed document types for this dependence
- `document_topic_ids` - Available topics for this dependence
- `system_ids` - Related systems
- `in_actual_nomenclator` - Whether this dependence is in the current institutional classifier

**Key Features:**

- Unique name constraint
- Configurable document types and topics per dependence
- Integration with institutional nomenclator system

#### 3. `tmc.document_type`

Types of documents that can be created.

**Key Fields:**

- `name` - Type name
- `abbreviation` - Short code used in document names
- `model` - Reference model for document type

#### 4. `tmc.document_topic`

Hierarchical topic/subject categorization system.

**Key Fields:**

- `name` - Topic name
- `parent_id` - Parent topic (for hierarchical structure)

**Key Features:**

- Supports parent-child relationships
- Main topics (no parent) and secondary topics (with parent)
- Used for categorizing documents

#### 5. `tmc.institutional_classifier`

Institutional nomenclator for organizing dependencies by period.

**Key Fields:**

- `period` - Year of the nomenclator
- `due_date` - When this nomenclator expires (empty for current)
- `dependence_order_ids` - Ordered list of dependencies
- `pdf` - Binary field for PDF document
- `document_id` - Related document

**Key Features:**

- Only one "current" nomenclator (with no due_date) at a time
- Automatically updates `in_actual_nomenclator` flag on dependencies
- Period validation (cannot be in the future)
- Prevents duplicate current nomenclators

#### 6. `tmc.employee`

Employee/personnel management.

**Key Fields:**

- Basic employee information
- Related to jobs and titles

#### 7. `tmc.office`

Office management within the organization.

#### 8. `tmc.highlight`

Document highlights/priorities for important tracking.

**Key Fields:**

- `document_id` - Related document
- Priority level (high, medium)

### Views Structure

The module includes comprehensive views for all models:

- Form views for data entry and editing
- List views for browsing records
- Search views with filters and grouping
- Menu structure organized by model

### Security

Security is defined through:

- `security/groups.xml` - User groups and roles
- `security/ir.model.access.csv` - Model-level access rights
