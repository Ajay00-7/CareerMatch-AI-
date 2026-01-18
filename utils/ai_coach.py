import os
import json
import random
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class AICoach:
    def __init__(self):
        self.knowledge_base = {}
        self.load_knowledge_base()
        
    def load_knowledge_base(self):
        """Load the offline knowledge base from JSON."""
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            data_path = os.path.join(base_dir, 'data', 'career_knowledge.json')
            
            with open(data_path, 'r', encoding='utf-8') as f:
                self.knowledge_base = json.load(f)
            logger.info("✅ Offline Knowledge Base loaded successfully!")
        except Exception as e:
            logger.error(f"❌ Failed to load Knowledge Base: {e}")
            self.knowledge_base = {}

    def generate_response(self, message, context=None):
        """
        Generate a response using the Offline Knowledge Base.
        """
        try:
            return self._generate_offline_response(message, context)
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return self._format_response("I encountered an error processing your request. Please try again.")

    def _generate_offline_response(self, message, context):
        """
        Rule-based logic to query the local knowledge base.
        """
        msg_lower = message.lower()
        
        # 0. Context Extraction
        skills = context.get('skills', []) if context else []
        job_matches = context.get('jobMatches', []) if context else []
        top_role_context = job_matches[0].get('job_title') if job_matches else None
        
        # 1. Greetings
        if any(w in msg_lower for w in ['hi', 'hello', 'hey', 'start', 'greetings']):
            greetings = self.knowledge_base.get('bot_personality', {}).get('greetings', [
                "Hello! I'm your Offline Career Coach. How can I help you today?"
            ])
            return self._format_response(random.choice(greetings))

        # 2. Identify Role from Message
        roles = self.knowledge_base.get('roles', {})
        detected_role = None
        
        # Check standard normalized names
        for role_name in roles.keys():
            if role_name.lower() in msg_lower:
                detected_role = role_name
                break
        
        # Check partial/alias matching if exact fail
        if not detected_role:
             aliases = {
                 'frontend': 'Frontend Developer',
                 'front end': 'Frontend Developer',
                 'backend': 'Backend Developer',
                 'back end': 'Backend Developer',
                 'fullstack': 'Full Stack Developer',
                 'full stack': 'Full Stack Developer',
                 'data scientist': 'Data Scientist',
                 'ml': 'Machine Learning Engineer',
                 'machine learning': 'Machine Learning Engineer',
                 'devops': 'DevOps Engineer'
             }
             for alias, full_name in aliases.items():
                 if alias in msg_lower:
                     detected_role = full_name
                     break
        
        # Fallback to context if user implies "it" or "that job" or generally asks without role
        if not detected_role and top_role_context:
            # Only assume context if strictly asking about "the job" or general vague queries
            if any(w in msg_lower for w in ['this', 'that', 'the job', 'my role', 'target', 'for me']):
                 # Try to match the context role to our DB
                 for role_name in roles.keys():
                    if role_name.lower() in top_role_context.lower():
                        detected_role = role_name
                        break

        # 3. Intent Handling
        
        # Intent: INTERVIEW PREP
        if any(w in msg_lower for w in ['interview', 'question', 'ask me', 'quiz']):
            if detected_role:
                questions = roles[detected_role].get('interview_questions', [])
                if questions:
                    selected = random.sample(questions, min(3, len(questions)))
                    reply = f"Here are some common interview questions for **{detected_role}** roles:\n\n"
                    for q in selected:
                        reply += f"• {q}\n"
                    reply += "\n💡 *Tip: Use the STAR method to answer behavioral questions!*"
                    return self._format_response(reply)
            elif 'interview' in msg_lower:
                 # General interview advice
                 tips = self.knowledge_base.get('general_advice', {}).get('interview_prep', [])
                 return self._format_response(
                     "For general interview prep, keep these in mind:\n\n" + 
                     "\n".join([f"• {t}" for t in tips[:3]]) + 
                     "\n\n*Specify a job role (e.g., 'interview questions for DevOps') for more details!*"
                 )

        # Intent: SALARY
        if any(w in msg_lower for w in ['salary', 'pay', 'compensat', 'earn', 'money']):
            if detected_role:
                salary = roles[detected_role].get('salary_range', 'Variable')
                return self._format_response(f"The typical salary range for a **{detected_role}** is:\n\n💰 **{salary}**\n\n*Note: This varies by location and experience level.*")
            else:
                return self._format_response("I can share salary insights! Please mention a role, e.g., **'Salary for Data Scientist'**.")

        # Intent: ROADMAP / LEARNING
        if any(w in msg_lower for w in ['roadmap', 'learn', 'study', 'path', 'become a']):
            if detected_role:
                roadmap = roles[detected_role].get('roadmap', [])
                return self._format_response(
                    f"Here is a recommended learning path for **{detected_role}**:\n\n" +
                    "\n".join(roadmap)
                )
            else:
                 return self._format_response("I can guide your learning! Ask me like: **'Roadmap for Backend Developer'**.")

        # Intent: SKILLS
        if any(w in msg_lower for w in ['skill', 'stack', 'know', 'technology']):
            if detected_role:
                skills_list = roles[detected_role].get('key_skills', [])
                return self._format_response(f"Key skills required for **{detected_role}** include:\n\n✅ " + ", ".join(skills_list))
            elif top_role_context:
                 # Use context 
                 return self._format_response(f"Based on your analysis, you should focus on skills for **{top_role_context}**. Ask me 'skills for {top_role_context}' to see the list!")

        # Intent: DESCRIPTION / "TELL ME ABOUT"
        if detected_role and any(w in msg_lower for w in ['what is', 'tell me about', 'describe', 'role']):
             desc = roles[detected_role].get('description', '')
             return self._format_response(f"**{detected_role}**: {desc}")

        # Intent: PROJECT ANALYSIS [NEW]
        if any(w in msg_lower for w in ['project', 'work', 'experience', 'portfolio', 'what did i do']):
            project_analysis = context.get('projectAnalysis', []) if context else []
            if project_analysis:
                reply = "Here is an analysis of your projects:\n\n"
                for p in project_analysis[:3]: # Limit to top 3
                    reply += f"📂 **{p['name']}** ({p['role']})\n"
                    if p.get('advantages'):
                        reply += f"✅ **Strengths:** {', '.join(p['advantages'][:2])}\n"
                    if p.get('disadvantages'):
                         reply += f"⚠️ **Improve:** {', '.join(p['disadvantages'][:1])}\n"
                    reply += "\n"
                reply += "💡 *Tip: Ensure you highlight the impact (metrics) of these projects in your interviews!*"
                return self._format_response(reply)
            elif top_role_context:
                 return self._format_response(f"I don't have your project details yet. Upload your resume and I can analyze how your work fits **{top_role_context}** roles!")

        # Intent: RESUME SUMMARY [NEW]
        summary_text = context.get('summary', '') if context else ''
        if 'summary' in msg_lower or 'summarize' in msg_lower:
            if summary_text:
                return self._format_response(f"📋 **Resume Summary:**\n\n{summary_text}")
            else:
                 return self._format_response("Please upload your resume first, and I'll generate a comprehensive summary for you.")

        # Intent: GENERAL ADVICE (Resume, Soft Skills)
        if 'resume' in msg_lower:
            tips = self.knowledge_base.get('general_advice', {}).get('resume', [])
            return self._format_response("📝 **Resume Tips:**\n" + "\n".join([f"• {t}" for t in tips]))
        
        if 'negotiat' in msg_lower:
             tips = self.knowledge_base.get('general_advice', {}).get('negotiation', [])
             return self._format_response("🤝 **Negotiation Tips:**\n" + "\n".join([f"• {t}" for t in tips]))
             
        # 4. Fallback (Context-Aware)
        if detected_role:
             return self._format_response(f"I'm listening! You can ask me about **interview questions**, **salary**, or **learning path** for {detected_role}.")
        elif top_role_context:
             return self._format_response(f"I'm not sure specifically, but for **{top_role_context}** roles, I can help with skills or interview prep. Try asking 'interview for {top_role_context}'!")
        
        fallbacks = self.knowledge_base.get('bot_personality', {}).get('fallback', ["I'm not sure about that."])
        return self._format_response(random.choice(fallbacks))

    def _format_response(self, text):
        """Standard response format."""
        return {
            "reply": text,
            "timestamp": datetime.now().strftime("%I:%M %p")
        }
