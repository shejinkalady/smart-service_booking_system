from database import create_connection
import hashlib


# ============================================================
# 1. LOGIN
# ============================================================

def login(connection):

    print("\n================================")
    print("          SMART SERVICE")
    print("             LOGIN")
    print("================================")

    email = input("Email: ").strip()
    password = input("Password: ").strip()

    password_hash = hashlib.sha256(
        password.encode()
    ).hexdigest()

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            user_id,
            name,
            email,
            role
        FROM users
        WHERE email = %s
          AND password_hash = %s
    """, (email, password_hash))

    user = cursor.fetchone()

    cursor.close()

    if not user:
        print("\n❌ Invalid email or password.")
        return None

    print("\n================================")
    print("       LOGIN SUCCESSFUL! ✅")
    print("================================")
    print(f"Welcome : {user['name']}")
    print(f"Role    : {user['role']}")
    print("================================")

    return user


# ============================================================
# 2. VIEW SERVICE CATEGORIES
# ============================================================

def show_categories(connection):

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            category_id,
            category_name,
            description
        FROM service_categories
        ORDER BY category_id
    """)

    categories = cursor.fetchall()

    print("\n================================")
    print("       SERVICE CATEGORIES")
    print("================================")

    if not categories:
        print("No categories found.")

    for category in categories:

        print(f"\n{category[0]}. {category[1]}")
        print(f"   {category[2]}")

    cursor.close()


# ============================================================
# 3. VIEW SERVICES
# ============================================================

def show_services(connection):

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            service_id,
            category_id,
            service_name,
            description,
            estimated_duration,
            price
        FROM services
        WHERE is_active = 1
        ORDER BY category_id, service_id
    """)

    services = cursor.fetchall()

    print("\n==============================")
    print("           SERVICES")
    print("==============================")

    if not services:

        print("No services found.")
        cursor.close()
        return

    for service in services:

        print(f"\nID: {service[0]}")
        print(f"Service: {service[2]}")
        print(f"Description: {service[3]}")
        print(f"Duration: {service[4]} minutes")
        print(f"Price: ₹{service[5]}")
        print("------------------------------")

    cursor.close()


# ============================================================
# 4. FIND PROVIDERS
# ============================================================

def find_providers(connection):

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            service_id,
            service_name,
            price
        FROM services
        WHERE is_active = 1
        ORDER BY service_id
    """)

    services = cursor.fetchall()

    print("\n========== FIND PROVIDERS ==========")

    if not services:

        print("No services available.")
        cursor.close()
        return

    print("\nAVAILABLE SERVICES")

    for service in services:

        print(
            f"{service[0]}. "
            f"{service[1]} - ₹{service[2]}"
        )

    service_id = input("\nEnter Service ID: ")

    cursor.execute("""
        SELECT
            p.provider_id,
            p.business_name,
            p.location,
            ps.price
        FROM provider_services ps
        JOIN providers p
            ON ps.provider_id = p.provider_id
        WHERE ps.service_id = %s
          AND ps.is_available = 1
    """, (service_id,))

    providers = cursor.fetchall()

    if not providers:

        print("\nNo providers available.")

    else:

        print("\n==============================")
        print("     AVAILABLE PROVIDERS")
        print("==============================")

        for i, provider in enumerate(providers, start=1):

            print(f"\n{i}. {provider[1]}")
            print(f"   Location: {provider[2]}")
            print(f"   Price: ₹{provider[3]}")
            print("------------------------------")

    cursor.close()


# ============================================================
# 5. CREATE BOOKING
# ============================================================

def create_booking(connection, customer_id, customer_name):

    cursor = connection.cursor()

    print("\n================================")
    print("          CREATE BOOKING")
    print("================================")

    print(f"Customer: {customer_name}")

    # --------------------------------------------------------
    # SHOW SERVICES
    # --------------------------------------------------------

    cursor.execute("""
        SELECT
            service_id,
            service_name,
            price
        FROM services
        WHERE is_active = 1
        ORDER BY service_id
    """)

    services = cursor.fetchall()

    if not services:

        print("\nNo services available.")
        cursor.close()
        return

    print("\n========== AVAILABLE SERVICES ==========")

    for i, service in enumerate(services, start=1):

        print(
            f"{i}. "
            f"{service[1]} - ₹{service[2]}"
        )

    try:

        service_choice = int(
            input("\nSelect Service: ")
        )

    except ValueError:

        print("\n❌ Invalid service selection.")
        cursor.close()
        return

    if service_choice < 1 or service_choice > len(services):

        print("\n❌ Invalid service selection.")
        cursor.close()
        return

    selected_service = services[
        service_choice - 1
    ]

    service_id = selected_service[0]
    service_name = selected_service[1]

    # --------------------------------------------------------
    # SHOW PROVIDERS
    # --------------------------------------------------------

    cursor.execute("""
        SELECT
            p.provider_id,
            p.business_name,
            p.location,
            ps.price
        FROM provider_services ps
        JOIN providers p
            ON ps.provider_id = p.provider_id
        WHERE ps.service_id = %s
          AND ps.is_available = 1
        ORDER BY p.provider_id
    """, (service_id,))

    providers = cursor.fetchall()

    if not providers:

        print("\nNo providers available.")
        cursor.close()
        return

    print("\n========== AVAILABLE PROVIDERS ==========")

    for i, provider in enumerate(providers, start=1):

        print(f"\n{i}. {provider[1]}")
        print(f"   Location: {provider[2]}")
        print(f"   Price: ₹{provider[3]}")
        print("----------------------------------------")

    try:

        provider_choice = int(
            input("\nSelect Provider: ")
        )

    except ValueError:

        print("\n❌ Invalid provider selection.")
        cursor.close()
        return

    if provider_choice < 1 or provider_choice > len(providers):

        print("\n❌ Invalid provider selection.")
        cursor.close()
        return

    selected_provider = providers[
        provider_choice - 1
    ]

    provider_id = selected_provider[0]
    provider_name = selected_provider[1]
    price = selected_provider[3]

    # --------------------------------------------------------
    # BOOKING DATE
    # --------------------------------------------------------

    booking_date = input(
        "\nEnter booking date (YYYY-MM-DD): "
    )

    # --------------------------------------------------------
    # AVAILABLE SLOTS
    # --------------------------------------------------------

    cursor.execute("""
        SELECT
            availability_id,
            start_time,
            end_time
        FROM availability
        WHERE provider_id = %s
          AND available_date = %s
          AND is_available = 1
        ORDER BY start_time
    """, (
        provider_id,
        booking_date
    ))

    slots = cursor.fetchall()

    if not slots:

        print(
            "\n❌ No available time slots "
            "for this date."
        )

        cursor.close()
        return

    print("\n========== AVAILABLE TIME SLOTS ==========")

    for i, slot in enumerate(slots, start=1):

        print(
            f"{i}. "
            f"{slot[1]} - {slot[2]}"
        )

    try:

        slot_choice = int(
            input("\nSelect Time Slot: ")
        )

    except ValueError:

        print("\n❌ Invalid time slot.")
        cursor.close()
        return

    if slot_choice < 1 or slot_choice > len(slots):

        print("\n❌ Invalid time slot.")
        cursor.close()
        return

    selected_slot = slots[
        slot_choice - 1
    ]

    availability_id = selected_slot[0]
    booking_time = selected_slot[1]

    # --------------------------------------------------------
    # CUSTOMER DETAILS
    # --------------------------------------------------------

    customer_email = input(
        "\nEnter your email: "
    )

    customer_note = input(
        "Enter any note: "
    )

    # --------------------------------------------------------
    # CREATE BOOKING
    # --------------------------------------------------------

    try:

        cursor.execute("""
            INSERT INTO bookings
            (
                customer_id,
                provider_id,
                service_id,
                availability_id,
                booking_date,
                booking_time,
                customer_email,
                status,
                customer_note,
                price
            )
            VALUES
            (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s
            )
        """, (
            customer_id,
            provider_id,
            service_id,
            availability_id,
            booking_date,
            booking_time,
            customer_email,
            "pending",
            customer_note,
            price
        ))

        booking_id = cursor.lastrowid

        cursor.execute("""
            UPDATE availability
            SET is_available = 0
            WHERE availability_id = %s
        """, (availability_id,))

        connection.commit()

        print("\n================================")
        print("       BOOKING CREATED! ✅")
        print("================================")
        print(f"Booking ID : {booking_id}")
        print(f"Service    : {service_name}")
        print(f"Provider   : {provider_name}")
        print(f"Date       : {booking_date}")
        print(f"Time       : {booking_time}")
        print(f"Price      : ₹{price}")
        print("Status     : pending")
        print("================================")

    except Exception as error:

        connection.rollback()

        print("\n❌ Booking failed.")
        print("Error:", error)

    cursor.close()


# ============================================================
# 6. VIEW CUSTOMER BOOKINGS
# ============================================================

def view_bookings(connection, customer_id):

    cursor = connection.cursor()

    print("\n================================")
    print("          MY BOOKINGS")
    print("================================")

    cursor.execute("""
        SELECT
            b.booking_id,
            s.service_name,
            p.business_name,
            b.booking_date,
            b.booking_time,
            b.price,
            b.status,
            b.customer_note
        FROM bookings b
        JOIN services s
            ON b.service_id = s.service_id
        JOIN providers p
            ON b.provider_id = p.provider_id
        WHERE b.customer_id = %s
        ORDER BY
            b.booking_date DESC,
            b.booking_time DESC
    """, (customer_id,))

    bookings = cursor.fetchall()

    if not bookings:

        print("\nNo bookings found.")
        cursor.close()
        return

    for booking in bookings:

        print("\n--------------------------------")
        print(f"Booking ID : {booking[0]}")
        print(f"Service    : {booking[1]}")
        print(f"Provider   : {booking[2]}")
        print(f"Date       : {booking[3]}")
        print(f"Time       : {booking[4]}")
        print(f"Price      : ₹{booking[5]}")
        print(f"Status     : {booking[6]}")
        print(f"Note       : {booking[7]}")
        print("--------------------------------")

    cursor.close()


# ============================================================
# 7. CANCEL BOOKING
# ============================================================

def cancel_booking(connection, customer_id):

    cursor = connection.cursor()

    print("\n========== CANCEL BOOKING ==========")

    booking_id = input(
        "Enter Booking ID to cancel: "
    )

    cursor.execute("""
        SELECT
            booking_id,
            availability_id,
            status
        FROM bookings
        WHERE booking_id = %s
          AND customer_id = %s
    """, (
        booking_id,
        customer_id
    ))

    booking = cursor.fetchone()

    if not booking:

        print("\n❌ Booking not found.")
        cursor.close()
        return

    availability_id = booking[1]
    current_status = booking[2]

    if current_status in (
        "completed",
        "cancelled",
        "rejected"
    ):

        print(
            f"\n❌ This booking is already "
            f"{current_status}."
        )

        cursor.close()
        return

    cursor.execute("""
        UPDATE bookings
        SET status = 'cancelled'
        WHERE booking_id = %s
          AND customer_id = %s
    """, (
        booking_id,
        customer_id
    ))

    # Release the time slot
    cursor.execute("""
        UPDATE availability
        SET is_available = 1
        WHERE availability_id = %s
    """, (availability_id,))

    connection.commit()

    print("\n================================")
    print("       BOOKING CANCELLED! ✅")
    print("================================")
    print(f"Booking ID : {booking_id}")
    print("Status     : cancelled")
    print("Time slot  : Released")
    print("================================")

    cursor.close()


# ============================================================
# 8. RESCHEDULE BOOKING
# ============================================================

def reschedule_booking(connection, customer_id):

    cursor = connection.cursor()

    print("\n========== RESCHEDULE BOOKING ==========")

    booking_id = input(
        "Enter Booking ID: "
    )

    # --------------------------------------------------------
    # FIND CURRENT BOOKING
    # --------------------------------------------------------

    cursor.execute("""
        SELECT
            booking_id,
            provider_id,
            service_id,
            availability_id,
            status
        FROM bookings
        WHERE booking_id = %s
          AND customer_id = %s
    """, (
        booking_id,
        customer_id
    ))

    booking = cursor.fetchone()

    if not booking:

        print("\n❌ Booking not found.")
        cursor.close()
        return

    provider_id = booking[1]
    old_availability_id = booking[3]
    status = booking[4]

    if status in (
        "cancelled",
        "completed",
        "rejected",
        "in_progress"
    ):

        print(
            f"\n❌ Booking cannot be rescheduled."
        )
        print(f"Current status: {status}")

        cursor.close()
        return

    # --------------------------------------------------------
    # NEW DATE
    # --------------------------------------------------------

    new_date = input(
        "\nEnter new booking date (YYYY-MM-DD): "
    )

    # --------------------------------------------------------
    # AVAILABLE SLOTS
    # --------------------------------------------------------

    cursor.execute("""
        SELECT
            availability_id,
            start_time,
            end_time
        FROM availability
        WHERE provider_id = %s
          AND available_date = %s
          AND is_available = 1
        ORDER BY start_time
    """, (
        provider_id,
        new_date
    ))

    slots = cursor.fetchall()

    if not slots:

        print("\n❌ No available slots.")
        cursor.close()
        return

    print("\n================================")
    print("       AVAILABLE TIME SLOTS")
    print("================================")

    for i, slot in enumerate(slots, start=1):

        print(
            f"{i}. "
            f"{slot[1]} - {slot[2]}"
        )

    try:

        choice = int(
            input("\nSelect time slot: ")
        )

    except ValueError:

        print("\n❌ Invalid selection.")
        cursor.close()
        return

    if choice < 1 or choice > len(slots):

        print("\n❌ Invalid time slot.")
        cursor.close()
        return

    selected_slot = slots[choice - 1]

    new_availability_id = selected_slot[0]
    new_time = selected_slot[1]

    # --------------------------------------------------------
    # UPDATE BOOKING
    # --------------------------------------------------------

    try:

        cursor.execute("""
            UPDATE bookings
            SET
                availability_id = %s,
                booking_date = %s,
                booking_time = %s,
                status = 'pending'
            WHERE booking_id = %s
              AND customer_id = %s
        """, (
            new_availability_id,
            new_date,
            new_time,
            booking_id,
            customer_id
        ))

        # New slot unavailable
        cursor.execute("""
            UPDATE availability
            SET is_available = 0
            WHERE availability_id = %s
        """, (new_availability_id,))

        # Old slot released
        cursor.execute("""
            UPDATE availability
            SET is_available = 1
            WHERE availability_id = %s
        """, (old_availability_id,))

        connection.commit()

        print("\n================================")
        print("      BOOKING RESCHEDULED! ✅")
        print("================================")
        print(f"Booking ID : {booking_id}")
        print(f"New Date   : {new_date}")
        print(f"New Time   : {new_time}")
        print("Status     : pending")
        print("================================")

    except Exception as error:

        connection.rollback()

        print("\n❌ Rescheduling failed.")
        print("Error:", error)

    cursor.close()


# ============================================================
# 9. PROVIDER DASHBOARD
# ============================================================

def provider_dashboard(connection, provider_id):

    cursor = connection.cursor()

    # --------------------------------------------------------
    # PROVIDER DETAILS
    # --------------------------------------------------------

    cursor.execute("""
        SELECT
            business_name,
            location
        FROM providers
        WHERE provider_id = %s
    """, (provider_id,))

    provider = cursor.fetchone()

    if not provider:

        print("\n❌ Provider profile not found.")
        cursor.close()
        return

    while True:

        print("\n================================")
        print("       PROVIDER DASHBOARD")
        print("================================")
        print(f"Business : {provider[0]}")
        print(f"Location : {provider[1]}")
        print("================================")

        print("1. View My Bookings")
        print("2. View Pending Bookings")
        print("3. Update Booking Status")
        print("4. Logout")

        choice = input("\nEnter your choice: ")

        # ----------------------------------------------------
        # VIEW BOOKINGS
        # ----------------------------------------------------

        if choice == "1":

            cursor.execute("""
                SELECT
                    b.booking_id,
                    s.service_name,
                    b.booking_date,
                    b.booking_time,
                    b.price,
                    b.status,
                    b.customer_note
                FROM bookings b
                JOIN services s
                    ON b.service_id = s.service_id
                WHERE b.provider_id = %s
                ORDER BY
                    b.booking_date DESC,
                    b.booking_time DESC
            """, (provider_id,))

            bookings = cursor.fetchall()

            print("\n========== MY BOOKINGS ==========")

            if not bookings:

                print("No bookings found.")

            else:

                for booking in bookings:

                    print("\n------------------------------")
                    print(f"Booking ID : {booking[0]}")
                    print(f"Service    : {booking[1]}")
                    print(f"Date       : {booking[2]}")
                    print(f"Time       : {booking[3]}")
                    print(f"Price      : ₹{booking[4]}")
                    print(f"Status     : {booking[5]}")
                    print(f"Note       : {booking[6]}")
                    print("------------------------------")

        # ----------------------------------------------------
        # PENDING BOOKINGS
        # ----------------------------------------------------

        elif choice == "2":

            cursor.execute("""
                SELECT
                    b.booking_id,
                    b.customer_id,
                    s.service_name,
                    b.booking_date,
                    b.booking_time,
                    b.price,
                    b.customer_note
                FROM bookings b
                JOIN services s
                    ON b.service_id = s.service_id
                WHERE b.provider_id = %s
                  AND b.status = 'pending'
                ORDER BY
                    b.booking_date,
                    b.booking_time
            """, (provider_id,))

            bookings = cursor.fetchall()

            print("\n========== PENDING BOOKINGS ==========")

            if not bookings:

                print("No pending bookings.")

            else:

                for booking in bookings:

                    print("\n------------------------------")
                    print(f"Booking ID : {booking[0]}")
                    print(f"Customer ID: {booking[1]}")
                    print(f"Service    : {booking[2]}")
                    print(f"Date       : {booking[3]}")
                    print(f"Time       : {booking[4]}")
                    print(f"Price      : ₹{booking[5]}")
                    print(f"Note       : {booking[6]}")
                    print("------------------------------")

        # ----------------------------------------------------
        # UPDATE STATUS
        # ----------------------------------------------------

        elif choice == "3":

            booking_id = input(
                "\nEnter Booking ID: "
            )

            cursor.execute("""
                SELECT
                    status,
                    availability_id
                FROM bookings
                WHERE booking_id = %s
                  AND provider_id = %s
            """, (
                booking_id,
                provider_id
            ))

            booking = cursor.fetchone()

            if not booking:

                print("\n❌ Booking not found.")
                continue

            current_status = booking[0]
            availability_id = booking[1]

            print(
                f"\nCurrent Status: "
                f"{current_status}"
            )

            if current_status in (
                "completed",
                "cancelled",
                "rejected"
            ):

                print(
                    "\n❌ This booking can no longer "
                    "be modified."
                )

                continue

            print("\n1. Accept")
            print("2. Reject")
            print("3. In Progress")
            print("4. Completed")
            print("5. Cancel")

            status_choice = input(
                "\nSelect new status: "
            )

            status_map = {
                "1": "accepted",
                "2": "rejected",
                "3": "in_progress",
                "4": "completed",
                "5": "cancelled"
            }

            if status_choice not in status_map:

                print("\n❌ Invalid choice.")
                continue

            new_status = status_map[
                status_choice
            ]

            # ------------------------------------------------
            # STATUS VALIDATION
            # ------------------------------------------------

            if current_status == "pending":

                if new_status not in (
                    "accepted",
                    "rejected",
                    "cancelled"
                ):

                    print(
                        "\n❌ Pending booking can only "
                        "be accepted, rejected or cancelled."
                    )

                    continue

            elif current_status == "accepted":

                if new_status not in (
                    "in_progress",
                    "cancelled"
                ):

                    print(
                        "\n❌ Accepted booking can only "
                        "move to in_progress or cancelled."
                    )

                    continue

            elif current_status == "in_progress":

                if new_status != "completed":

                    print(
                        "\n❌ In-progress booking can only "
                        "be completed."
                    )

                    continue

            # ------------------------------------------------
            # UPDATE STATUS
            # ------------------------------------------------

            cursor.execute("""
                UPDATE bookings
                SET status = %s
                WHERE booking_id = %s
                  AND provider_id = %s
            """, (
                new_status,
                booking_id,
                provider_id
            ))

            # Release slot if provider rejects/cancels
            if new_status in (
                "rejected",
                "cancelled"
            ):

                cursor.execute("""
                    UPDATE availability
                    SET is_available = 1
                    WHERE availability_id = %s
                """, (availability_id,))

            connection.commit()

            print("\n================================")
            print("       STATUS UPDATED! ✅")
            print("================================")
            print(f"Booking ID : {booking_id}")
            print(f"Old Status : {current_status}")
            print(f"New Status : {new_status}")
            print("================================")

        # ----------------------------------------------------
        # LOGOUT
        # ----------------------------------------------------

        elif choice == "4":

            print("\nLogging out...")
            break

        else:

            print("\n❌ Invalid choice.")

    cursor.close()


# ============================================================
# 10. CUSTOMER DASHBOARD
# ============================================================

def customer_dashboard(connection, user):

    customer_id = user["user_id"]
    customer_name = user["name"]

    while True:

        print("\n================================")
        print("       CUSTOMER DASHBOARD")
        print("================================")
        print(f"Welcome, {customer_name}")
        print("================================")

        print("1. View Service Categories")
        print("2. View Services")
        print("3. Find Providers")
        print("4. Create Booking")
        print("5. View My Bookings")
        print("6. Cancel Booking")
        print("7. Reschedule Booking")
        print("8. Logout")

        choice = input("\nEnter your choice: ")

        if choice == "1":

            show_categories(connection)

        elif choice == "2":

            show_services(connection)

        elif choice == "3":

            find_providers(connection)

        elif choice == "4":

            create_booking(
                connection,
                customer_id,
                customer_name
            )

        elif choice == "5":

            view_bookings(
                connection,
                customer_id
            )

        elif choice == "6":

            cancel_booking(
                connection,
                customer_id
            )

        elif choice == "7":

            reschedule_booking(
                connection,
                customer_id
            )

        elif choice == "8":

            print("\nLogging out...")
            break

        else:

            print("\n❌ Invalid choice.")


# ============================================================
# 11. MAIN
# ============================================================

def main():

    connection = create_connection()

    if connection is None:

        print("❌ Database connection failed.")
        return

    user = login(connection)

    if user is None:

        connection.close()
        return

    # ========================================================
    # CUSTOMER
    # ========================================================

    if user["role"] == "customer":

        customer_dashboard(
            connection,
            user
        )

    # ========================================================
    # PROVIDER
    # ========================================================

    elif user["role"] == "provider":

        cursor = connection.cursor()

        cursor.execute("""
            SELECT provider_id
            FROM providers
            WHERE user_id = %s
        """, (user["user_id"],))

        provider = cursor.fetchone()

        cursor.close()

        if not provider:

            print(
                "\n❌ Provider profile not found."
            )

        else:

            provider_id = provider[0]

            provider_dashboard(
                connection,
                provider_id
            )

    else:

        print(
            "\n❌ Unknown user role."
        )

    connection.close()

    print("\n================================")
    print("     THANK YOU FOR USING")
    print("        SMART SERVICE")
    print("================================")


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":
    main()



    