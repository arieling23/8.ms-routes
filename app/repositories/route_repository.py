from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.route import Route
from app.logger import logger  

class RouteRepository:

    @staticmethod
    async def get_all_routes(session: AsyncSession):
        try:
            result = await session.execute(select(Route))
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Error al obtener rutas: {e}")
            return []

    @staticmethod
    async def get_route_by_id(session: AsyncSession, route_id: int):
        try:
            result = await session.execute(select(Route).where(Route.id == route_id))
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Error al obtener ruta con ID {route_id}: {e}")
            return None

    @staticmethod
    async def delete_route(session: AsyncSession, route_id: int) -> bool:
        try:
            route = await RouteRepository.get_route_by_id(session, route_id)
            if route:
                await session.delete(route)
                await session.commit()
                return True
            return False
        except Exception as e:
            logger.error(f"Error al eliminar ruta con ID {route_id}: {e}")
            return False
