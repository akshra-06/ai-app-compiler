
from app.schemas.integration_schema import (
    IntegrationDefinition,
    IntegrationAction,
    IntegrationTrigger
)


INTEGRATION_REGISTRY = {

    "slack": IntegrationDefinition(

        id="slack",

        displayName="Slack",

        authType="oauth2",

        triggers=[

            IntegrationTrigger(
                event="record_created",
                description=
                    "Triggered when a record is created"
            ),

            IntegrationTrigger(
                event="status_changed",
                description=
                    "Triggered when status changes"
            )
        ],

        actions=[

            IntegrationAction(

                id="send_message",

                description=
                    "Send message to Slack channel",

                inputSchema={
                    "channel": "string",
                    "message": "string"
                },

                outputSchema={
                    "success": "boolean"
                }
            ),

            IntegrationAction(

                id="send_dm",

                description=
                    "Send direct message",

                inputSchema={
                    "user": "string",
                    "message": "string"
                },

                outputSchema={
                    "success": "boolean"
                }
            )
        ]
    ),

    "gmail": IntegrationDefinition(

        id="gmail",

        displayName="Gmail",

        authType="oauth2",

        triggers=[

            IntegrationTrigger(
                event="record_created",
                description=
                    "Triggered when record created"
            )
        ],

        actions=[

            IntegrationAction(

                id="send_email",

                description=
                    "Send email notification",

                inputSchema={
                    "to": "string",
                    "subject": "string",
                    "body": "string"
                },

                outputSchema={
                    "success": "boolean"
                }
            )
        ]
    ),

    "stripe": IntegrationDefinition(

        id="stripe",

        displayName="Stripe",

        authType="api_key",

        triggers=[

            IntegrationTrigger(
                event="payment_created",
                description=
                    "Payment event"
            )
        ],

        actions=[

            IntegrationAction(

                id="create_customer",

                description=
                    "Create Stripe customer",

                inputSchema={
                    "email": "string"
                },

                outputSchema={
                    "customerId": "string"
                }
            )
        ]
    ),

    "whatsapp": IntegrationDefinition(

        id="whatsapp",

        displayName="WhatsApp",

        authType="api_key",

        triggers=[

            IntegrationTrigger(
                event="status_changed",
                description=
                    "Triggered on status update"
            )
        ],

        actions=[

            IntegrationAction(

                id="send_template_message",

                description=
                    "Send WhatsApp template",

                inputSchema={
                    "phone": "string",
                    "template": "string"
                },

                outputSchema={
                    "success": "boolean"
                }
            )
        ]
    ),

    "webhook": IntegrationDefinition(

        id="webhook",

        displayName="Generic Webhook",

        authType="webhook_secret",

        triggers=[

            IntegrationTrigger(
                event="any",
                description=
                    "Any event"
            )
        ],

        actions=[

            IntegrationAction(

                id="post_payload",

                description=
                    "POST payload to webhook URL",

                inputSchema={
                    "url": "string",
                    "payload": "object"
                },

                outputSchema={
                    "status": "number"
                }
            )
        ]
    )
}

