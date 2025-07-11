from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models.route import Route, Segment
from app.logger import logger

class RouteService:

    @staticmethod
    async def create(session: AsyncSession, name: str, segments_data: list[dict]):
        try:
            new_route = Route(name=name)

            for segment in segments_data:
                new_segment = Segment(
                    origin=segment["origin"],
                    destination=segment["destination"],
                    distance_km=segment["distanceKm"]  # ✅ acceso por clave
                )
                new_route.segments.append(new_segment)

            session.add(new_route)
            await session.commit()

            result = await session.execute(
                select(Route)
                .options(selectinload(Route.segments))
                .where(Route.id == new_route.id)
            )
            return result.scalar_one()

        except Exception as e:
            logger.error(f"Error al crear la ruta: {e}")
            await session.rollback()
            raise e

    @staticmethod
    async def get_all(session: AsyncSession):
        try:
            result = await session.execute(
                select(Route).options(selectinload(Route.segments))
            )
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Error al obtener rutas: {e}")
            return []
