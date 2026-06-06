from app.schemas import ChatResponse, Recommendation


class ResponseFormatter:
    def clarification(self, reply: str) -> ChatResponse:
        return ChatResponse(
            reply=reply,
            recommendations=[],
            end_of_conversation=False
        )

    def refusal(self, reply: str) -> ChatResponse:
        return ChatResponse(
            reply=reply,
            recommendations=[],
            end_of_conversation=False
        )

    def recommendations(
        self,
        reply: str,
        items: list[dict],
        end_of_conversation: bool = False
    ) -> ChatResponse:
        recommendations = [
            Recommendation(
                name=item.get("name", ""),
                url=item.get("url", ""),
                test_type=item.get("test_type")
            )
            for item in items[:10]
        ]

        return ChatResponse(
            reply=reply,
            recommendations=recommendations,
            end_of_conversation=end_of_conversation
        )