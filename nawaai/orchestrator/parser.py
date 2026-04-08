"""Spec file parsing."""

import json
import re
from typing import Any, Dict, List, Optional, Tuple

from .models import (
    AcceptanceCriterion,
    CorrectnessProperty,
    Design,
    PBTSpecification,
    Requirement,
    Spec,
    SpecStatus,
    Task,
    TaskStatus,
    TestType,
)


class SpecParser:
    """Parses spec files."""

    def __init__(self):
        """Initialize the parser."""
        self.errors: List[str] = []

    def parse_requirements(self, content: str) -> Tuple[str, Dict[str, str], List[Requirement]]:
        """
        Parse requirements.md file.

        Returns:
            Tuple of (introduction, glossary, requirements)
        """
        self.errors = []

        # Extract introduction
        intro_match = re.search(r"## Introduction\n(.*?)(?=## Glossary|\Z)", content, re.DOTALL)
        introduction = intro_match.group(1).strip() if intro_match else ""

        # Extract glossary
        glossary = self._parse_glossary(content)

        # Extract requirements
        requirements = self._parse_requirements_list(content)

        return introduction, glossary, requirements

    def _parse_glossary(self, content: str) -> Dict[str, str]:
        """Parse glossary section."""
        glossary = {}
        glossary_match = re.search(r"## Glossary\n(.*?)(?=## Requirements|\Z)", content, re.DOTALL)

        if glossary_match:
            glossary_text = glossary_match.group(1)
            # Parse glossary items (format: - **Term**: Definition)
            for line in glossary_text.split("\n"):
                if line.startswith("- **"):
                    match = re.match(r"- \*\*([^*]+)\*\*:\s*(.*)", line)
                    if match:
                        term, definition = match.groups()
                        glossary[term] = definition.strip()

        return glossary

    def _parse_requirements_list(self, content: str) -> List[Requirement]:
        """Parse requirements list."""
        requirements = []
        req_match = re.search(r"## Requirements\n(.*)", content, re.DOTALL)

        if not req_match:
            return requirements

        req_text = req_match.group(1)

        # Split by requirement headers (### Requirement N:)
        req_blocks = re.split(r"### Requirement (\d+):", req_text)

        for i in range(1, len(req_blocks), 2):
            req_id = f"R{req_blocks[i]}"
            req_content = req_blocks[i + 1] if i + 1 < len(req_blocks) else ""

            # Extract user story
            user_story_match = re.search(r"\*\*User Story:\*\*(.*?)(?=####|\Z)", req_content, re.DOTALL)
            user_story = user_story_match.group(1).strip() if user_story_match else ""

            # Extract acceptance criteria
            criteria = self._parse_acceptance_criteria(req_content)

            if user_story or criteria:
                requirements.append(
                    Requirement(
                        id=req_id,
                        user_story=user_story,
                        acceptance_criteria=criteria,
                    )
                )

        return requirements

    def _parse_acceptance_criteria(self, content: str) -> List[AcceptanceCriterion]:
        """Parse acceptance criteria."""
        criteria = []
        criteria_match = re.search(r"#### Acceptance Criteria\n(.*?)(?=###|\Z)", content, re.DOTALL)

        if not criteria_match:
            return criteria

        criteria_text = criteria_match.group(1)

        # Parse numbered criteria (1. WHEN ... THEN ...)
        for line in criteria_text.split("\n"):
            if line.strip().startswith(("1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.")):
                # Extract criterion ID and description
                match = re.match(r"\d+\.\s*(.*)", line.strip())
                if match:
                    description = match.group(1)
                    criterion_id = f"AC{len(criteria) + 1}"
                    criteria.append(
                        AcceptanceCriterion(
                            id=criterion_id,
                            description=description,
                            testable=True,
                        )
                    )

        return criteria

    def parse_design(self, content: str) -> Design:
        """Parse design.md file."""
        # Extract overview
        overview_match = re.search(r"## Overview\n(.*?)(?=## Architecture|\Z)", content, re.DOTALL)
        overview = overview_match.group(1).strip() if overview_match else ""

        # Extract key principles
        principles = []
        principles_match = re.search(r"### Key Design Principles\n(.*?)(?=##|\Z)", content, re.DOTALL)
        if principles_match:
            principles_text = principles_match.group(1)
            for line in principles_text.split("\n"):
                if line.startswith("- "):
                    principles.append(line[2:].strip())

        # Extract architecture
        arch_match = re.search(r"## Architecture\n(.*?)(?=## Components|\Z)", content, re.DOTALL)
        architecture = arch_match.group(1).strip() if arch_match else ""

        # Extract correctness properties
        properties = self._parse_correctness_properties(content)

        return Design(
            overview=overview,
            key_principles=principles,
            architecture=architecture,
            correctness_properties=properties,
        )

    def _parse_correctness_properties(self, content: str) -> List[CorrectnessProperty]:
        """Parse correctness properties."""
        properties = []
        props_match = re.search(r"## Correctness Properties\n(.*?)(?=## Error Handling|\Z)", content, re.DOTALL)

        if not props_match:
            return properties

        props_text = props_match.group(1)

        # Split by property headers (### Property N:)
        prop_blocks = re.split(r"### Property (\d+):", props_text)

        for i in range(1, len(prop_blocks), 2):
            prop_id = f"P{prop_blocks[i]}"
            prop_content = prop_blocks[i + 1] if i + 1 < len(prop_blocks) else ""

            # Extract title
            title_match = re.search(r"^(.*?)\n", prop_content)
            title = title_match.group(1).strip() if title_match else ""

            # Extract statement
            statement_match = re.search(r"\*For any\*(.*?)(?=\*\*Validates:|\Z)", prop_content, re.DOTALL)
            statement = statement_match.group(1).strip() if statement_match else ""

            # Extract validates
            validates_match = re.search(r"\*\*Validates:\s*(.*?)\*\*", prop_content)
            validates = []
            if validates_match:
                validates_text = validates_match.group(1)
                validates = [v.strip() for v in validates_text.split(",")]

            if title or statement:
                properties.append(
                    CorrectnessProperty(
                        id=prop_id,
                        title=title,
                        statement=statement,
                        validates=validates,
                        test_type="property",
                    )
                )

        return properties

    def parse_tasks(self, content: str, category: str, spec_name: str) -> List[Task]:
        """Parse tasks.md file."""
        tasks = []
        task_blocks = re.split(r"- \[\s*\]\s+(\d+(?:\.\d+)?)\.\s+(.*?)(?=- \[|\Z)", content, flags=re.DOTALL)

        for i in range(1, len(task_blocks), 2):
            task_id = task_blocks[i]
            task_content = task_blocks[i + 1] if i + 1 < len(task_blocks) else ""

            # Extract description
            desc_match = re.match(r"(.*?)\n", task_content)
            description = desc_match.group(1).strip() if desc_match else ""

            # Extract requirements traceability
            req_match = re.search(r"_Requirements:\s*(.*?)_", task_content)
            requirements_traceability = []
            if req_match:
                req_text = req_match.group(1)
                requirements_traceability = [r.strip() for r in req_text.split(",")]

            # Extract PBT specification
            pbt_spec = self._parse_pbt_specification(task_content)

            # Extract dependencies
            dependencies = []
            dep_match = re.search(r"Dependencies:\s*(.*?)(?:\n|$)", task_content)
            if dep_match:
                dep_text = dep_match.group(1)
                dependencies = [d.strip() for d in dep_text.split(",") if d.strip()]

            if description:
                tasks.append(
                    Task(
                        id=task_id,
                        description=description,
                        status=TaskStatus.NOT_STARTED,
                        category=category,
                        spec_name=spec_name,
                        spec_category=category,
                        requirements_traceability=requirements_traceability,
                        dependencies=dependencies,
                        pbt_specification=pbt_spec,
                    )
                )

        return tasks

    def _parse_pbt_specification(self, content: str) -> Optional[PBTSpecification]:
        """Parse PBT specification."""
        framework_match = re.search(r"Framework:\s*(\w+)", content)
        if not framework_match:
            return None

        framework = framework_match.group(1)
        iterations_match = re.search(r"Iterations:\s*(\d+)", content)
        iterations = int(iterations_match.group(1)) if iterations_match else 100

        properties_match = re.search(r"Properties:\s*([\d,\s]+)", content)
        properties = []
        if properties_match:
            props_text = properties_match.group(1)
            properties = [p.strip() for p in props_text.split(",")]

        return PBTSpecification(
            framework=framework,
            iterations=iterations,
            properties=properties,
        )

    def parse_bugfix(self, content: str) -> Dict[str, Any]:
        """Parse bugfix.md file."""
        bugfix_data = {}

        # Extract bug condition
        bug_match = re.search(r"## Bug Condition\n(.*?)(?=## Expected Behavior|\Z)", content, re.DOTALL)
        if bug_match:
            bugfix_data["bug_condition"] = bug_match.group(1).strip()

        # Extract expected behavior
        expected_match = re.search(r"## Expected Behavior\n(.*?)(?=## Fix Implementation|\Z)", content, re.DOTALL)
        if expected_match:
            bugfix_data["expected_behavior"] = expected_match.group(1).strip()

        # Extract fix implementation
        fix_match = re.search(r"## Fix Implementation\n(.*?)(?=##|\Z)", content, re.DOTALL)
        if fix_match:
            bugfix_data["fix_implementation"] = fix_match.group(1).strip()

        return bugfix_data

    def parse_config(self, content: str) -> Dict[str, Any]:
        """Parse .config.kiro file."""
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            self.errors.append(f"Error parsing config: {e}")
            return {}

    def get_errors(self) -> List[str]:
        """Get all parsing errors."""
        return self.errors
