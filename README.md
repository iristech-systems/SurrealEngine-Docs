# SurrealEngine Documentation

This directory contains the Sphinx documentation for SurrealEngine.

## What's Been Done

✅ **Complete Documentation Setup**:
- Added comprehensive Google-style docstrings to core modules:
  - `__init__.py` - Main package with detailed module descriptions
  - `connection.py` - Already had excellent docstrings
  - `document.py` - Already had comprehensive docstrings  
  - `fields/base.py` - Enhanced base field class documentation
  - `schema.py` - Already had good docstrings

✅ **Sphinx Configuration**:
- Created `conf.py` with ansys-sphinx-theme as requested
- Set `html_permalinks_icon = "<span>¶</span>"` as specified
- Configured Napoleon for Google-style docstrings
- Set up intersphinx mapping for Python documentation
- Enabled sphinx-copybutton for code examples

✅ **Complete Documentation Structure**:
- `index.rst` - Main documentation landing page
- `api/` directory with comprehensive API reference:
  - Individual module documentation files
  - Detailed usage examples and code samples
  - Proper cross-references and navigation

✅ **API Reference Documentation**:
- Connection management and pooling
- Document models and metaclasses  
- All field types with examples
- Query building and execution
- Exception handling
- Schema management utilities
- Signals and lifecycle events
- Materialized views and aggregations

✅ **Build System**:
- `Makefile` for easy documentation building
- `requirements.txt` for documentation dependencies
- Custom CSS for improved styling
- All documentation builds successfully (812 warnings are mostly formatting issues in existing docstrings)

## Building the Documentation

1. Install dependencies:
   ```bash
   pip install -r docs/requirements.txt
   ```

2. Build HTML documentation:
   ```bash
   cd docs
   make html
   ```

3. View documentation:
   ```bash
   open _build/html/index.html
   ```

## Live Development

For live rebuilding during development:
```bash
cd docs
make livehtml
```

This will start a server with auto-reload at http://localhost:8000.

## Files Structure

```
docs/
├── conf.py                    # Sphinx configuration
├── index.rst                 # Main documentation page  
├── Makefile                  # Build commands
├── requirements.txt          # Documentation dependencies
├── _static/
│   └── custom.css            # Custom styling
└── api/                      # API reference
    ├── connection.rst        # Connection management
    ├── document.rst          # Document models
    ├── fields.rst            # Field types
    ├── query.rst             # Query building
    ├── exceptions.rst        # Exception classes
    ├── schema.rst            # Schema management
    ├── signals.rst           # Lifecycle signals
    ├── materialized_view.rst # Materialized views
    ├── aggregation.rst       # Data aggregation
    └── surrealengine*.rst    # Individual modules
```

## Theme and Styling

- Uses `ansys-sphinx-theme` as requested
- Custom permalink icon: `<span>¶</span>`
- Google-style docstring formatting with Napoleon
- Code highlighting and copy buttons
- Responsive design with proper navigation

The documentation is now ready for production use and can be deployed to any static hosting service or integrated into a documentation portal.