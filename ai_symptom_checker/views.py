from rest_framework import views, permissions, status
from rest_framework.response import Response
from django.conf import settings
import hashlib
import json
import logging
from groq import Groq
from .models import SymptomCheck, SymptomCache
from .serializers import SymptomCheckSerializer, SymptomCheckRequestSerializer

logger = logging.getLogger(__name__)


class SymptomCheckerView(views.APIView):
    """
    AI Symptom Checker endpoint using Groq LLM
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def analyze_symptoms_with_groq(self, symptoms):
        """
        Analyze symptoms using Groq LLM API
        """
        try:
            api_key = settings.GROQ_API_KEY
            model = settings.GROQ_MODEL
            
            if not api_key:
                logger.warning("Groq API key not configured, using fallback response")
                return None
            
            logger.info(f"Calling Groq API with model: {model}")
            client = Groq(api_key=api_key)
            
            # Create a comprehensive prompt for symptom analysis
            prompt = f"""You are a medical assistant helping rural patients in India. Analyze the following symptoms and provide:
1. Top 3-5 probable medical conditions (with confidence scores as percentages between 0 and 1)
2. Recommendations for immediate care
3. When to seek urgent medical attention

Symptoms: {symptoms}

IMPORTANT: You MUST respond ONLY with valid JSON, no additional text. Use this exact structure:
{{
    "probable_conditions": [
        {{"condition": "Condition Name", "probability": 0.65, "description": "Brief explanation"}},
        {{"condition": "Another Condition", "probability": 0.25, "description": "Brief explanation"}}
    ],
    "recommendations": "Detailed recommendations for the patient",
    "urgency_level": "low",
    "when_to_see_doctor": "Guidance on when medical consultation is needed"
}}

Guidelines:
- Be conservative with medical advice
- Always recommend consulting a doctor for proper diagnosis
- Consider rural healthcare context (limited resources, distance to hospitals)
- Provide practical, actionable advice
- Use simple language that's easy to understand
- Return ONLY the JSON object, no markdown, no code blocks"""
            
            # Call Groq API
            logger.info("Sending request to Groq API...")
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful medical assistant providing preliminary symptom analysis. Always emphasize consulting a qualified doctor for proper diagnosis. Always respond with valid JSON only."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=model,
                temperature=0.3,  # Lower temperature for more consistent medical advice
                max_tokens=1500
            )
            
            response_text = chat_completion.choices[0].message.content
            logger.info(f"Groq API response received: {response_text[:200]}...")
            
            # Try to parse JSON from response
            try:
                # Extract JSON from markdown code blocks if present
                if "```json" in response_text:
                    json_start = response_text.find("```json") + 7
                    json_end = response_text.find("```", json_start)
                    response_text = response_text[json_start:json_end].strip()
                elif "```" in response_text:
                    json_start = response_text.find("```") + 3
                    json_end = response_text.find("```", json_start)
                    response_text = response_text[json_start:json_end].strip()
                
                result = json.loads(response_text)
                logger.info("Successfully parsed JSON from Groq response")
                
                # Format the response
                formatted_result = {
                    "probable_conditions": result.get("probable_conditions", []),
                    "recommendations": result.get("recommendations", "Please consult with a doctor for proper diagnosis."),
                    "urgency_level": result.get("urgency_level", "medium"),
                    "when_to_see_doctor": result.get("when_to_see_doctor", "If symptoms persist or worsen, consult a doctor immediately.")
                }
                
                # Extract confidence scores
                confidence_scores = {}
                for condition in formatted_result["probable_conditions"]:
                    condition_name = condition.get("condition", "")
                    probability = condition.get("probability", 0)
                    confidence_scores[condition_name] = probability
                
                formatted_result["confidence_scores"] = confidence_scores
                
                logger.info(f"Successfully formatted Groq response with {len(formatted_result['probable_conditions'])} conditions")
                return formatted_result
                
            except json.JSONDecodeError as je:
                # If JSON parsing fails, log the error and try to extract information from text
                logger.error(f"Failed to parse JSON from Groq response: {str(je)}")
                logger.error(f"Response text: {response_text}")
                # Still return the text as recommendations
                return {
                    "probable_conditions": [
                        {"condition": "Medical Consultation Required", "probability": 1.0, "description": "AI analysis completed - parsing error occurred"}
                    ],
                    "recommendations": response_text if response_text else "Please consult with a doctor for proper diagnosis.",
                    "urgency_level": "medium",
                    "when_to_see_doctor": "Please consult with a doctor for proper diagnosis.",
                    "confidence_scores": {"Medical Consultation Required": 1.0}
                }
                
        except Exception as e:
            logger.error(f"Error calling Groq API: {str(e)}", exc_info=True)
            return None
    
    def post(self, request):
        serializer = SymptomCheckRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        symptoms = serializer.validated_data['symptoms']
        
        # Check if user wants to bypass cache
        bypass_cache = request.query_params.get('bypass_cache', 'false').lower() == 'true'
        
        # Create hash for caching
        symptom_hash = hashlib.sha256(symptoms.encode()).hexdigest()
        
        # Check cache first (unless bypassed)
        if not bypass_cache:
            try:
                cached_result = SymptomCache.objects.get(symptom_hash=symptom_hash)
                cached_result.hit_count += 1
                cached_result.save()
                
                # Create symptom check record
                SymptomCheck.objects.create(
                    user=request.user,
                    symptoms=symptoms,
                    probable_conditions=cached_result.probable_conditions,
                    confidence_scores=cached_result.confidence_scores,
                    recommendations=cached_result.recommendations
                )
                
                return Response({
                    'probable_conditions': cached_result.probable_conditions,
                    'confidence_scores': cached_result.confidence_scores,
                    'recommendations': cached_result.recommendations,
                    'cached': True
                })
            except SymptomCache.DoesNotExist:
                pass
        else:
            logger.info("Cache bypassed by user request")
        
        # Analyze symptoms using Groq LLM
        logger.info(f"Analyzing symptoms for user {request.user.id}: {symptoms}")
        analysis_result = self.analyze_symptoms_with_groq(symptoms)
        
        # Fallback to basic response if Groq fails
        if not analysis_result:
            logger.warning("Groq API unavailable or failed, using fallback response")
            probable_conditions = [
                {"condition": "Medical Consultation Required", "probability": 1.0, "description": "Please consult with a doctor for proper diagnosis"}
            ]
            recommendations = "Please consult with a doctor for proper diagnosis. Rest and stay hydrated. If symptoms are severe, seek immediate medical attention."
            urgency_level = "medium"
            when_to_see_doctor = "If symptoms persist or worsen, consult a doctor immediately."
            confidence_scores = {}
        else:
            probable_conditions = analysis_result.get("probable_conditions", [])
            recommendations = analysis_result.get("recommendations", "Please consult with a doctor for proper diagnosis.")
            urgency_level = analysis_result.get("urgency_level", "medium")
            when_to_see_doctor = analysis_result.get("when_to_see_doctor", "If symptoms persist or worsen, consult a doctor immediately.")
            confidence_scores = analysis_result.get("confidence_scores", {})
            logger.info(f"Groq analysis successful: {len(probable_conditions)} conditions found")
        
        # Cache the result
        SymptomCache.objects.create(
            symptom_hash=symptom_hash,
            symptoms=symptoms,
            probable_conditions=probable_conditions,
            confidence_scores=confidence_scores,
            recommendations=recommendations
        )
        
        # Create symptom check record
        SymptomCheck.objects.create(
            user=request.user,
            symptoms=symptoms,
            probable_conditions=probable_conditions,
            confidence_scores=confidence_scores,
            recommendations=recommendations
        )
        
        return Response({
            'probable_conditions': probable_conditions,
            'confidence_scores': confidence_scores,
            'recommendations': recommendations,
            'urgency_level': urgency_level,
            'when_to_see_doctor': when_to_see_doctor,
            'cached': False
        })


class SymptomCheckHistoryView(views.APIView):
    """
    Get user's symptom check history
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        checks = SymptomCheck.objects.filter(user=request.user).order_by('-created_at')[:20]
        serializer = SymptomCheckSerializer(checks, many=True)
        return Response(serializer.data)
