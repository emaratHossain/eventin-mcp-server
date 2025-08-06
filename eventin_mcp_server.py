import logging
from typing import Any, List, Optional
import httpx
from mcp.server.fastmcp import FastMCP

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    filename='booking_server.log',
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize MCP server
mcp = FastMCP("event-bookings")

class BookingService:
    def __init__(self):
        self.base_url = "http://release.local/wp-json/eventin/v2/orders"
        self.client = httpx.AsyncClient(timeout=30.0)

    async def fetch_bookings(self, page: int = 1, per_page: int = 10) -> Optional[List[dict]]:
        """Fetch bookings from Eventin API"""
        try:
            params = {
                "paged": page,
                "per_page": per_page,
                "_locale": "user"
            }
            response = await self.client.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error: {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
        return None

booking_service = BookingService()

@mcp.tool()
async def get_bookings(
    page: int = 1,
    per_page: int = 10,
    status: Optional[str] = None,
    event_id: Optional[str] = None
) -> str:
    """
    Get event bookings with filters
    
    Args:
        page: Page number (default 1)
        per_page: Items per page (default 10)
        status: Filter by payment status (e.g., 'completed', 'failed')
        event_id: Filter by specific event ID
    """
    if bookings := await booking_service.fetch_bookings(page, per_page):
        filtered = []
        for booking in bookings:
            # Apply filters if provided
            if status and booking.get("status") != status:
                continue
            if event_id and str(booking.get("event_id")) != str(event_id):
                continue
                
            filtered.append(format_booking(booking))
        
        if not filtered:
            return "No bookings match your filters"
            
        return "\n\n---\n\n".join(filtered)
    return "Failed to fetch bookings"

def format_booking(booking: dict) -> str:
    """Format a single booking into readable string"""
    ticket_info = "\n".join(
        f"- {t['etn_ticket_name']} (Qty: {t['etn_ticket_qty']}, ${t['etn_ticket_price']})"
        for t in booking.get("ticket_items", [])
    )
    
    return f"""📅 Booking ID: {booking['id']}
👤 Customer: {booking['customer_fname']} {booking['customer_lname']}
📧 Email: {booking['customer_email']}
📞 Phone: {booking['customer_phone'] or 'Not provided'}

🎟️ Event: {booking['event_name']} (ID: {booking['event_id']})
🗓️ Date: {booking['date_time']}
💳 Payment: {booking['payment_method'].upper()} ({booking['status']})
💰 Total: ${booking['total_price']}

Tickets:
{ticket_info}"""

@mcp.tool()
async def get_booking_stats() -> str:
    """Get summary statistics of bookings"""
    if bookings := await booking_service.fetch_bookings(per_page=100):  # Get more records for stats
        status_counts = {}
        event_counts = {}
        total_revenue = 0
        
        for booking in bookings:
            status = booking.get("status")
            event_id = booking.get("event_id")
            
            status_counts[status] = status_counts.get(status, 0) + 1
            event_counts[event_id] = event_counts.get(event_id, 0) + 1
            
            if booking.get("status") == "completed":
                try:
                    total_revenue += float(booking.get("total_price", 0))
                except (TypeError, ValueError):
                    pass
        
        stats = [
            f"📊 Total Bookings: {len(bookings)}",
            "\n🔹 By Status:",
            *[f"- {status}: {count}" for status, count in status_counts.items()],
            "\n🔹 By Event:",
            *[f"- Event {event_id}: {count}" for event_id, count in event_counts.items()],
            f"\n💰 Estimated Revenue: ${total_revenue:.2f}"
        ]
        
        return "\n".join(stats)
    return "Failed to fetch booking statistics"

if __name__ == "__main__":
    try:
        logger.info("Starting Booking MCP Server")
        mcp.run(transport='stdio')
    except Exception as e:
        logger.critical(f"Server crashed: {e}", exc_info=True)
        raise