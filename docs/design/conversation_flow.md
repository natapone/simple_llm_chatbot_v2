# Pre-Sales Chatbot Conversation Flow Design Document

## Overview

This document outlines the detailed conversation flow for the pre-sales chatbot. It defines the conversation states, transitions, prompt strategies, and handling of both standard and non-standard project inquiries. This design will serve as the foundation for creating the system prompt and implementing the chatbot's behavior.

## Conversation States

The conversation will flow through these primary states:

1. **Greeting & Initial Need Assessment**
2. **Project Requirements Exploration**
3. **Timeline Discussion**
4. **Budget Discussion**
5. **Contact Information Collection**
6. **Follow-up Consent**
7. **Closing**

## Detailed State Descriptions

### 1. Greeting & Initial Need Assessment

**Purpose:** Establish rapport and identify the client's primary need.

**Entry Point:**
- User initiates conversation

**Bot Actions:**
- Greet the user warmly
- Ask about their business needs

**Example Prompts:**
- "Hi there! I'd love to help with your software development needs. What kind of project are you looking for?"
- "Hello! Welcome to our software development service. What can I help you with today?"

**User Response Handling:**
- If user mentions specific project type (website, app, etc.) → Move to Project Requirements
- If user is vague → Ask clarifying question: "Could you tell me a bit more about what you're looking for?"
- If user asks about the company first → Provide brief company info, then redirect: "Now, what kind of project are you interested in?"

### 2. Project Requirements Exploration

**Purpose:** Gather detailed information about the project scope and features.

**Entry Conditions:**
- User has indicated general project type

**Bot Actions:**
- Ask about specific features needed
- Explore project scope
- Identify business type if not already mentioned

**Example Prompts:**
- "What specific features would you like in your [project type]?"
- "Are you looking for a basic [project type] or something with more advanced features like [examples]?"
- "What kind of business will this [project type] be for?"

**Branching Logic:**
- **For standard project types:**
  - **Websites:** E-commerce, informational, portfolio
  - **Mobile apps:** Customer-facing, internal tools
  - **Custom software:** Business systems, integrations

- **For non-standard project types:**
  - Ask more detailed, open-ended questions
  - Focus on understanding unique requirements
  - Collect comprehensive information for custom assessment

**User Response Handling:**
- If user provides clear requirements → Note features, move to Timeline
- If user is uncertain → Offer examples: "Many clients with [business type] typically need features like [examples]. Would those be helpful?"
- If user asks about technical feasibility → Provide reassurance and examples of similar projects

### 3. Timeline Discussion

**Purpose:** Understand the client's timeline expectations and provide realistic guidance.

**Entry Conditions:**
- Basic project requirements established

**Bot Actions:**
- Ask about timeline expectations
- For standard projects: Provide realistic timeline guidance based on project type
- For non-standard projects: Record timeline expectations without validation

**Example Prompts:**
- Standard: "What's your expected timeline for launching this [project type]?"
- Non-standard: "For specialized projects like this, timelines can vary. When would you ideally like to have this completed?"

**Timeline Guidance Tool Integration:**
- For standard projects:
  - Use `get_timeline_guidance(project_type)` to retrieve appropriate timeline ranges
  - Format and present the guidance in a conversational way
- For non-standard projects:
  - Skip the guidance tool
  - Record the client's timeline expectations for later assessment

**User Response Handling:**
- If timeline is realistic → Acknowledge and move to Budget
- If timeline is too short (standard projects only) → Gently suggest more realistic timeframe
- If user has no timeline in mind → For standard projects, suggest typical timeline; for non-standard, emphasize need for custom assessment

### 4. Budget Discussion

**Purpose:** Understand the client's budget expectations and provide appropriate guidance.

**Entry Conditions:**
- Timeline expectations discussed

**Bot Actions:**
- Ask about budget expectations
- For standard projects: Provide budget guidance based on project type and requirements
- For non-standard projects: Record budget expectations without validation

**Example Prompts:**
- Standard: "Do you have a budget range in mind for this project?"
- Non-standard: "For unique projects like this, our team would need to provide a custom quote. Do you have a general budget range you're working with?"

**Budget Guidance Tool Integration:**
- For standard projects:
  - Use `get_budget_guidance(project_type)` to retrieve appropriate budget ranges
  - Format and present the guidance in a conversational way
- For non-standard projects:
  - Skip the guidance tool
  - Record the client's budget expectations for later assessment

**User Response Handling:**
- If budget is within guidance range (standard projects) → Acknowledge and move to Contact Information
- If budget is too low (standard projects) → Gently educate about realistic costs
- If user has no budget in mind → For standard projects, provide guidance; for non-standard, explain the need for custom assessment
- If user expresses budget concerns → Suggest phased approach or alternative solutions

### 5. Contact Information Collection

**Purpose:** Collect contact details for follow-up while respecting privacy concerns.

**Entry Conditions:**
- Project requirements, timeline, and budget discussed

**Bot Actions:**
- Ask for name and contact information
- Explain why this information is needed
- For non-standard projects: Emphasize the value of expert consultation

**Example Prompts:**
- Standard: "Great! To provide you with more specific information, could you share your name and the best way to contact you?"
- Non-standard: "Given the specialized nature of your project, it would be valuable to have one of our senior consultants review your requirements. Could you share your name and the best way to contact you?"

**User Response Handling:**
- If user provides contact info → Thank them and move to Follow-up Consent
- If user hesitates → Reassure about privacy: "We respect your privacy and will only use your information to follow up about this project."
- If user refuses → Accept gracefully and move to Closing without storing lead

### 6. Follow-up Consent

**Purpose:** Obtain explicit consent for follow-up communication.

**Entry Conditions:**
- User has provided contact information

**Bot Actions:**
- Explicitly ask for consent to follow up
- Explain what the follow-up will entail
- For non-standard projects: Explain the specialized assessment process

**Example Prompts:**
- Standard: "Thanks [name]! Do you agree to receive a follow-up from our team about your [project type]?"
- Non-standard: "Would it be okay if one of our specialists reaches out to discuss your unique project requirements in more detail?"

**User Response Handling:**
- If user consents → Thank them and move to Closing (with lead storage)
- If user declines → Thank them and move to Closing (without lead storage)
- If user asks questions about the follow-up → Provide details about the process

### 7. Closing

**Purpose:** End the conversation positively and set expectations for next steps.

**Entry Conditions:**
- Contact information and follow-up consent handled

**Bot Actions:**
- Thank the user for their time
- Set expectations for next steps
- Offer additional assistance

**Example Prompts:**
- Standard: "Thank you for sharing your project details! Our team will reach out to you soon. Is there anything else I can help you with today?"
- Non-standard: "Thank you for sharing your specialized project requirements. Our expert team will review them and reach out to discuss further. Is there anything else you'd like to know in the meantime?"

**User Response Handling:**
- If user has more questions → Answer and continue conversation
- If user says goodbye → End conversation
- If user is silent → After timeout, provide closing message

## Special Handling Cases

### 1. Non-Standard Project Types

**Detection:**
- Project doesn't match predefined categories
- Budget/timeline guidance tools return empty results
- Project requires specialized expertise

**Approach:**
- Collect comprehensive requirements through open-ended questions
- Skip standard guidance tools for budget and timeline
- Record client expectations without validation
- Flag the lead for custom assessment
- Emphasize the need for expert consultation during contact collection

**Example Conversation Segment:**
```
User: I need a virtual reality training simulator for medical students.

Bot: That sounds like an interesting specialized project. Could you tell me more about the specific training scenarios you'd like to simulate?

User: We want to simulate surgical procedures and emergency response situations.

Bot: That's fascinating! Would these simulations need to include haptic feedback, realistic medical tools, or integration with any existing medical systems?
```

### 2. Early Budget/Timeline Questions

**Detection:**
- User asks about pricing or timeline before requirements are discussed

**Approach:**
- Acknowledge the question
- Explain that accurate estimates depend on requirements
- Gently guide back to requirements discussion
- Return to the question once requirements are established

**Example Conversation Segment:**
```
User: How much does a website cost?

Bot: That's a great question. Website costs vary significantly based on your specific needs and features. To give you an accurate estimate, I'd like to understand your requirements better first. What kind of website are you looking for?
```

### 3. Multi-Information Messages

**Detection:**
- User provides multiple pieces of information in one message

**Approach:**
- Acknowledge all information received
- Ask about any missing critical information
- Follow the flow based on what's still needed

**Example Conversation Segment:**
```
User: I need an e-commerce website for my clothing store. I want to launch in 2 months with a budget around $2000.

Bot: Thanks for sharing those details about your clothing store e-commerce website, timeline, and budget! To better understand your needs, could you tell me what specific features you'd like in your online store? For example, would you need product variations, customer accounts, or any special payment methods?
```

### 4. Off-Topic Questions

**Detection:**
- User asks questions unrelated to project requirements

**Approach:**
- Briefly answer if possible
- Gently guide back to the conversation flow

**Example Conversation Segment:**
```
User: Do you also do logo design?

Bot: Yes, we do offer logo design as part of our branding services. Now, returning to your website project, could you tell me more about the specific features you'd need?
```

## Guidance Tool Integration

### Budget Guidance Integration

**For Standard Projects:**
1. Identify the project type from the conversation
2. Call `get_budget_guidance(project_type)`
3. Format the response using `format_budget_guidance()`
4. Present the information conversationally: "For a project like yours with [features], we typically see budgets ranging from $[min_budget] to $[max_budget]."

**For Non-Standard Projects:**
1. Skip the guidance tool
2. Use general language: "For specialized projects like this, costs can vary significantly based on the specific requirements."
3. Record the client's budget expectations without validation

### Timeline Guidance Integration

**For Standard Projects:**
1. Identify the project type from the conversation
2. Call `get_timeline_guidance(project_type)`
3. Format the response using `format_timeline_guidance()`
4. Present the information conversationally: "Based on your requirements, a project like this typically takes [min_timeline] to [max_timeline] to complete."

**For Non-Standard Projects:**
1. Skip the guidance tool
2. Use general language: "For specialized projects like this, timelines can vary based on the complexity and specific requirements."
3. Record the client's timeline expectations without validation

## Lead Storage Criteria

The chatbot will only trigger lead storage when ALL of these conditions are met:
1. Client name has been collected
2. Contact information (email or phone) has been collected
3. Explicit consent for follow-up has been received
4. Basic project requirements have been discussed

## Lead Data Structure

For all projects (standard and non-standard):
```json
{
  "timestamp": "ISO datetime",
  "client_name": "String",
  "client_business": "String",
  "contact_information": "String",
  "project_description": "String",
  "features": ["String"],
  "timeline": "String",
  "budget_range": "String",
  "confirmed_follow_up": "Boolean",
  "is_standard_project": "Boolean",
  "requires_custom_assessment": "Boolean",
  "additional_notes": "String"
}
```

## Decision Tree Diagram

```
Start
│
├─ Greeting & Initial Need Assessment
│  ├─ Standard project identified → Standard flow
│  │  │
│  │  ├─ Project Requirements Exploration
│  │  │  └─ Collect specific requirements based on project type
│  │  │
│  │  ├─ Timeline Discussion
│  │  │  └─ Use timeline guidance tool
│  │  │
│  │  └─ Budget Discussion
│  │     └─ Use budget guidance tool
│  │
│  └─ Non-standard project identified → Non-standard flow
│     │
│     ├─ Project Requirements Exploration (Enhanced)
│     │  └─ Ask more detailed, open-ended questions
│     │
│     ├─ Timeline Discussion (Modified)
│     │  └─ Skip timeline guidance tool
│     │
│     └─ Budget Discussion (Modified)
│        └─ Skip budget guidance tool
│
├─ Contact Information Collection
│  └─ For non-standard: Emphasize expert consultation
│
├─ Follow-up Consent
│  └─ For non-standard: Explain specialized assessment
│
└─ Closing
   └─ Set appropriate expectations based on project type
```

## Implementation Considerations for Prompt Creation

1. **Context Awareness:** The prompt should instruct the LLM to maintain awareness of the conversation state and what information has already been collected.

2. **Natural Transitions:** Transitions between states should feel conversational, not like filling out a form.

3. **Flexible Information Gathering:** The LLM should recognize when information is volunteered out of sequence and adapt accordingly.

4. **Project Type Detection:** The prompt should include guidance on how to detect standard vs. non-standard project types.

5. **Tool Usage Instructions:** Clear instructions on when and how to use the guidance tools, including handling cases where tools return no results.

6. **Tone Consistency:** Maintain a friendly, helpful, and professional tone throughout all conversation states.

7. **Error Recovery:** Include strategies for recovering from misunderstandings or unclear user inputs.

8. **Memory Utilization:** Instruct the LLM to reference previously collected information to avoid redundant questions.

9. **Lead Qualification:** Provide clear criteria for when a lead is considered qualified for storage.

10. **Specialized Project Handling:** Detailed instructions on the different approach for non-standard projects.

## Example Conversations

See the `Brief/Example conversation.txt` file for complete example conversations that demonstrate this flow in action. These examples show how the chatbot should handle different types of inquiries while maintaining a natural conversation flow.

## Relationship to System Prompt

This conversation flow design will be translated into the system prompt that guides the LLM's behavior. The system prompt will:

1. Define the chatbot's role and overall goals
2. Outline the conversation states and transitions
3. Provide instructions for using the guidance tools
4. Specify the criteria for lead storage
5. Include strategies for handling special cases

The system prompt should be reviewed and updated periodically based on conversation performance and feedback.

## Maintenance and Updates

When updating the conversation flow:

1. Document changes in this design document
2. Update the system prompt accordingly
3. Test the changes with various conversation scenarios
4. Monitor the impact on lead quality and conversion rates

## Conclusion

This conversation flow design provides a structured yet flexible approach that feels natural to users while ensuring all necessary lead information is collected. By handling both standard and non-standard project inquiries effectively, the chatbot can maximize lead generation while providing a positive user experience. 