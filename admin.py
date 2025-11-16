from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base
from models.hotel import Hotel
from models.room import Room
from models.customer import Customer
from models.booking import Booking
from models.report import Report


class Admin(Base):
    __tablename__ = "admins"

    adminID = Column(Integer, primary_key=True)
    hotel_id = Column(Integer, ForeignKey("hotels.hotelID"))

    
    hotelManaged = relationship("Hotel", back_populates="admin")

    

    def manageRoom(self, session, action, room=None):
        """
        Admin manages rooms: add, update, delete
        - action: "add", "update", "delete"
        """
        if action == "add":
            session.add(room)
            session.commit()
            return "Room added successfully!"

        elif action == "update":
            session.commit()
            return "Room updated successfully!"

        elif action == "delete":
            session.delete(room)
            session.commit()
            return "Room deleted!"

        return "Invalid action!"

    def manageCustomer(self, session, action, customer=None):
        """
        Manage customers: add, update, delete
        """
        if action == "add":
            session.add(customer)
            session.commit()
            return "Customer added!"

        elif action == "update":
            session.commit()
            return "Customer updated!"

        elif action == "delete":
            session.delete(customer)
            session.commit()
            return "Customer deleted!"

        return "Invalid action!"

    def manageBooking(self, session, action, booking=None):
        """
        Manage bookings: confirm, cancel, update
        """
        if action == "add":
            session.add(booking)
            session.commit()
            return "Booking created!"

        elif action == "update":
            session.commit()
            return "Booking updated!"

        elif action == "delete":
            session.delete(booking)
            session.commit()
            return "Booking deleted!"

        return "Invalid action!"

    def viewReport(self, session):
        """
        View ALL reports
        """
        reports = session.query(Report).all()
        return reports

    def generateReport(self, session, startDate, endDate):
        """
        Generate report based on:
        - total revenue (sum of bookings)
        - total bookings
        - available rooms
        """
        bookings = (
            session.query(Booking)
            .filter(Booking.checkInDate >= startDate)
            .filter(Booking.checkOutDate <= endDate)
            .all()
        )

        total_revenue = sum([b.totalPrice for b in bookings])
        total_bookings = len(bookings)

        available_rooms = (
            session.query(Room)
            .filter(Room.status == "available")
            .count()
        )

        new_report = Report(
            generatedDate=startDate,
            totalRevenue=total_revenue,
            totalBookings=total_bookings,
            availableRooms=available_rooms
        )

        session.add(new_report)
        session.commit()

        return new_report
