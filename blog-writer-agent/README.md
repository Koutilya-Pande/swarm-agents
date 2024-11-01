# Blog Writer Agent Workflow

This document outlines the detailed workflow of the Blog Writer Agent system, which automates the creation of a blog post from topic selection to final quality assurance. The workflow leverages a series of specialized AI agents, each responsible for a distinct part of the process.

## Workflow Steps

### 1. **Initiation by Admin Agent**
   - **Input**: User provides a blog topic.
   - **Action**: The Admin Agent initiates the project with a vision and sets guidelines for the task.
   - **Output**: Admin hands over the project to the Planner Agent for structure development.

### 2. **Planning by Planner Agent**
   - **Action**: Creates a comprehensive outline, organizing the blog into logical sections.
   - **Output**: Passes the structured outline to the Researcher Agent.

### 3. **Researching by Researcher Agent**
   - **Input**: Outline from Planner Agent.
   - **Action**: Performs a web search using the Tavily API to gather information for each section of the outline.
   - **Output**: Compiled research notes are handed to the Content Writer Agent.

### 4. **Writing by Content Writer Agent**
   - **Input**: Outline and research notes from the Researcher Agent.
   - **Action**: Composes a cohesive, informative draft, synthesizing information from research.
   - **Output**: Transfers the draft to the SEO Agent for optimization.

### 5. **SEO Optimization by SEO Agent**
   - **Input**: Draft and list of relevant keywords.
   - **Action**: Enhances the draft by incorporating keywords, optimizing headings, subheadings, and content for better SEO visibility.
   - **Output**: Sends the optimized draft to the Editor Agent.

### 6. **Editing by Editor Agent**
   - **Input**: SEO-optimized draft.
   - **Action**: Reviews the draft for readability, clarity, and grammar, improving narrative flow and quality.
   - **Output**: Passes the polished draft to the Quality Assurance Agent.

### 7. **Quality Assurance by Quality Assurance Agent**
   - **Input**: Final draft from the Editor Agent.
   - **Action**: Conducts a thorough review for accuracy and quality, ensuring high standards.
   - **Output**: If approved, the blog post is saved as a Markdown file using the `save_blog_post` function.

### 8. **Completion**
   - **Final Output**: The blog post is saved in the file system, and the user is informed of the successful creation of the post.

## Workflow Diagram

```plaintext
User Input: Blog Topic
        |
        v
   [Admin Agent]
        |
        v
   [Planner Agent]
        |
        v
[Researcher Agent]
        |
        v
[Content Writer Agent]
        |
        v
    [SEO Agent]
        |
        v
  [Editor Agent]
        |
        v
[Quality Assurance Agent]
        |
        v
  Save Blog Post (Markdown)
