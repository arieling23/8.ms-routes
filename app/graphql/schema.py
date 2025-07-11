import strawberry
from typing import List
from strawberry.types import Info
from app.services.route_service import RouteService
from app.graphql.types import RouteType, SegmentInput
from app.auth.dependencies import get_current_user

@strawberry.type
class Query:
    @strawberry.field
    async def getRoutes(self, info: Info) -> List[RouteType]:
        session = info.context["session"]
        return await RouteService.get_all(session)

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def createRoute(
        self,
        info: Info,
        name: str,
        segments_data: List[SegmentInput]
    ) -> RouteType:
        user = get_current_user(info.context["request"])
        if user["role"] != "admin":
            raise Exception("Access denied")

        session = info.context["session"]
        return await RouteService.create(session, name, [s.__dict__ for s in segments_data])

schema = strawberry.Schema(query=Query, mutation=Mutation)
