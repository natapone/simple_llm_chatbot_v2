# Chatbot Usage Guide

This guide provides instructions on how to use the Simple LLM Chatbot v2 effectively.

## Getting Started

### Accessing the Chatbot

1. Ensure the server is running with `uvicorn app.main:app --reload`
2. Open your web browser and navigate to `http://localhost:8000`
3. You should see the chat interface with a welcome message

### Basic Interaction

The chatbot is designed to assist with pre-sales inquiries for a software development company. You can ask questions about:

- Project budgets
- Development timelines
- Features and capabilities
- Technical requirements
- General information about software development

## Example Conversations

### Asking About Budget

**User**: "How much does it cost to build an e-commerce website?"

**Chatbot**: "For an e-commerce website, the budget typically ranges from $5,000 to $15,000. This includes basic e-commerce functionality with product listings and payment processing. The actual cost may vary depending on specific requirements, complexity, and customization needs."

### Asking About Timeline

**User**: "How long does it take to build a corporate website?"

**Chatbot**: "Building a corporate website typically takes between 4 weeks to 2 months. This timeline includes design, development, content creation, and testing phases. The exact duration depends on the complexity of the site, specific requirements, and the approval process."

### Discussing Project Requirements

**User**: "I need a blog website for my business. What features should I consider?"

**Chatbot**: "For a blog website, you might want to consider these key features:
1. Content management system
2. Responsive design for mobile devices
3. SEO optimization
4. Social media integration
5. Comment section
6. Newsletter subscription
7. Search functionality
8. Analytics integration

Would you like more information about any of these features or have specific requirements in mind?"

## Lead Generation

The chatbot is designed to collect lead information during conversations. When you provide details about:

- Your name
- Business name
- Contact information
- Project description
- Budget expectations
- Timeline requirements

This information is stored in the database and can be viewed in the leads dashboard.

## Accessing the Leads Dashboard

1. Click on the "View Leads Dashboard" link in the chat interface
2. Or navigate directly to `http://localhost:8000/leads`
3. The dashboard displays all collected leads with their details

## Tips for Effective Use

1. **Be specific**: The more specific your questions, the more accurate the responses will be.
2. **Provide context**: Mention the type of project you're interested in (e-commerce, corporate, blog, etc.).
3. **Ask follow-up questions**: If you need more details, ask follow-up questions to get more specific information.
4. **Share requirements**: Sharing your specific requirements helps the chatbot provide more tailored responses.
5. **Explore options**: Ask about different approaches or technologies to understand trade-offs.

## Limitations

The chatbot has some limitations to be aware of:

1. It may not have information about highly specialized or niche project types.
2. Budget and timeline estimates are general ranges and may vary based on specific requirements.
3. The chatbot cannot provide legally binding quotes or commitments.
4. Technical details are simplified for general understanding.

## Troubleshooting

If you encounter issues with the chatbot:

1. **Refresh the page**: If the chat interface becomes unresponsive, try refreshing the page.
2. **Check server logs**: If the server is running with the `--reload` flag, check the terminal for error messages.
3. **Restart the server**: If problems persist, restart the server with `uvicorn app.main:app --reload`.
4. **Clear browser cache**: If the interface appears outdated, clear your browser cache.

## API Integration

For programmatic access to the chatbot, you can use the API endpoint:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user123", "message": "How much does it cost to build an e-commerce website?", "session_id": null}'
```

For more details on API usage, see the [API Documentation](../api/endpoints.md).

## Feedback and Support

If you have feedback or need support with the chatbot:

1. Report issues on the project's issue tracker
2. Contribute improvements via pull requests
3. Contact the development team for feature requests 