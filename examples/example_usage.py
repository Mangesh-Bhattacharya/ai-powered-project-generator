#!/usr/bin/env python3
"""
Example usage of the Project Generator
"""

from project_generator import ProjectGenerator
import json

def main():
    # Initialize generator
    generator = ProjectGenerator()
    
    print("=" * 60)
    print("AI-Powered Project Generator - Example Usage")
    print("=" * 60)
    
    # Example 1: Generate a random cybersecurity project
    print("\n1. Generating a random Cybersecurity project (Intermediate)...")
    project1 = generator.generate_project(
        domain="cybersecurity",
        experience_level="intermediate"
    )
    print(f"\nProject: {project1['title']}")
    print(f"Duration: {project1['duration']}")
    print(f"Tech Stack: {', '.join(project1['tech_stack'])}")
    
    # Example 2: Generate project with tech preferences
    print("\n" + "=" * 60)
    print("\n2. Generating Data Analytics project with Python & ML...")
    project2 = generator.generate_project(
        domain="data_analytics",
        experience_level="beginner",
        tech_preferences=["Python", "Machine Learning"]
    )
    print(f"\nProject: {project2['title']}")
    print(f"Description: {project2['description'][:100]}...")
    
    # Example 3: Generate project with duration constraint
    print("\n" + "=" * 60)
    print("\n3. Generating AI project (max 3 weeks)...")
    project3 = generator.generate_project(
        domain="artificial_intelligence",
        experience_level="beginner",
        duration_weeks=3
    )
    print(f"\nProject: {project3['title']}")
    print(f"Duration: {project3['duration']}")
    
    # Example 4: Get all projects in a domain
    print("\n" + "=" * 60)
    print("\n4. Getting all Cloud Security projects...")
    cloud_projects = generator.get_all_projects(domain="cloud_security")
    print(f"\nFound {len(cloud_projects)} Cloud Security projects:")
    for idx, proj in enumerate(cloud_projects, 1):
        print(f"  {idx}. {proj['title']} ({proj['difficulty']})")
    
    # Example 5: Export project plan
    print("\n" + "=" * 60)
    print("\n5. Exporting project plan to Markdown...")
    markdown_plan = generator.export_project_plan(project1, "markdown")
    
    # Save to file
    filename = f"{project1['title'].lower().replace(' ', '_')}_plan.md"
    with open(filename, 'w') as f:
        f.write(markdown_plan)
    print(f"\nProject plan saved to: {filename}")
    
    # Example 6: Get statistics
    print("\n" + "=" * 60)
    print("\n6. Project Database Statistics...")
    all_projects = generator.get_all_projects()
    
    domains = {}
    difficulties = {}
    techs = {}
    
    for proj in all_projects:
        # Count by domain
        domain = proj.get('domain', 'Unknown')
        domains[domain] = domains.get(domain, 0) + 1
        
        # Count by difficulty
        difficulty = proj.get('difficulty', 'Unknown')
        difficulties[difficulty] = difficulties.get(difficulty, 0) + 1
        
        # Count technologies
        for tech in proj.get('tech_stack', []):
            techs[tech] = techs.get(tech, 0) + 1
    
    print(f"\nTotal Projects: {len(all_projects)}")
    print(f"\nProjects by Domain:")
    for domain, count in sorted(domains.items()):
        print(f"  {domain.replace('_', ' ').title()}: {count}")
    
    print(f"\nProjects by Difficulty:")
    for difficulty, count in sorted(difficulties.items()):
        print(f"  {difficulty}: {count}")
    
    print(f"\nTop 10 Technologies:")
    sorted_techs = sorted(techs.items(), key=lambda x: x[1], reverse=True)[:10]
    for tech, count in sorted_techs:
        print(f"  {tech}: {count} projects")
    
    print("\n" + "=" * 60)
    print("\nExample usage complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
