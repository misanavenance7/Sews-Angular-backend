import json
import logging
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('graphql_requests')

class LogGraphQLRequestMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.content_type == 'application/json':
            try:
                # Decode the request body as a string first
                raw_data = request.body.decode('utf-8')
                
                # Load it into a Python dictionary (this ensures valid JSON)
                request_body = json.loads(raw_data)
                
                # Log the JSON pretty-printed (without escape characters)
                logger.debug(f"Incoming GraphQL request: {json.dumps(request_body, indent=2)}")
                
            except json.JSONDecodeError:
                logger.error("Error decoding request body as JSON")
            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}")
