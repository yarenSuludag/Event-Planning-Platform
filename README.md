# Smart Event Planning Platform

A web-based platform that enables users to create events, participate in them, and build a social interaction network. The system is designed to provide personalized recommendations based on user interests and past events, while integrating advanced features like map services and route planning.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture & Tech Stack](#architecture--tech-stack)
- [System Flow](#system-flow)
- [Testing and Results](#testing-and-results)
- [Future Enhancements](#future-enhancements)
- [Documentation & References](#documentation--references)
- [Contributing](#contributing)
- [License](#license)
- [Getting Started](#getting-started)


---

## Overview

In today’s fast-paced digital world, there is an increasing need for online platforms that simplify the organization of events and enhance social interactions. The **Smart Event Planning Platform** is built to meet these needs by allowing users to:

- **Create and manage events:** Users can easily create events, share them, and manage their participation.
- **Interact socially:** The platform supports group chats and one-to-one messaging around events, fostering community connections.
- **Receive personalized recommendations:** Based on interests and event history, the system suggests events that match user preferences.
- **Utilize advanced map features:** Integrated with Google Maps API, the platform offers location visualization and optimal route planning.
- **Prevent scheduling conflicts:** A built-in algorithm ensures that overlapping events are flagged, enhancing scheduling efficiency.

---

## Features

- **User Management:**  
  - Custom user registration and authentication (extends Django’s AbstractUser with additional fields such as phone number, profile picture, and interests).  
  - Profile management with update capabilities.

- **Event Management:**  
  - Create, update, and delete events with details such as name, description, date, duration, location, and category.  
  - Conflict detection to avoid overlapping event schedules.

- **Messaging System:**  
  - Event-based chat rooms that allow only event participants to communicate.  
  - Persistent chat history accessible to users.

- **Rule-Based Recommendation System:**  
  - Provides event suggestions based on user interests, past participation, and geographical proximity.

- **Map and Route Planning:**  
  - Integration with Google Maps API to display event locations.  
  - Route planning features to determine the most efficient travel paths.

---

## Architecture & Tech Stack

- **Backend:**  
  - Developed using the Django framework.  
  - Implements RESTful APIs for seamless integration of system components.  
  - Custom models for user and event management.

- **Database:**  
  - Managed with MySQL using Django’s ORM to ensure data integrity and performance optimization.

- **Frontend:**  
  - Designed with HTML, CSS, and Bootstrap for a responsive and user-friendly interface.  
  - Django templating is used for dynamic content rendering.

- **External Integrations:**  
  - Google Maps API for map visualization and route planning.

---

## System Flow

The platform follows a clear user journey, as illustrated in the flow diagrams below:

1. **Homepage Visit:**  
   - The system checks if the user is logged in.  
   - If logged in, personalized content and recommendations are displayed; otherwise, login and registration options are provided.

2. **User Registration/Login:**  
   - Users can register via a dedicated form, which is validated before account creation.  
   - Login functionality authenticates users and redirects them to the homepage.

3. **Event Management:**  
   - Users can create new events by filling out a form with event details.  
   - Conflict detection ensures no overlapping event schedules.  
   - Existing events can be updated or deleted as needed.

4. **Messaging:**  
   - Each event includes a chat room where participants can exchange messages and view previous conversations.

---

### Screenshots

![Flow Diagram 1](path/to/your/picture1.png)  
![Flow Diagram 2](path/to/your/picture2.png)

---

## Testing and Results

- **User Management:**  
  Successful registration, login, and profile updates were achieved without issues.

- **Event Management:**  
  Users can create, modify, and delete events with accurate conflict detection.

- **Recommendation System:**  
  Personalized event suggestions based on user interests and location are effectively provided.

- **Map Integration:**  
  Event locations are correctly visualized on the map, with efficient route planning functionality.

- **Messaging:**  
  Real-time and historical message exchanges within event-specific chats work seamlessly.

Overall, tests confirm that the platform offers an easy-to-use and efficient solution for event planning and social networking.

---

## Future Enhancements

- **Machine Learning Integration:**  
  Enhance the recommendation algorithms using machine learning techniques.

- **Mobile Application:**  
  Develop a mobile version of the platform to increase accessibility.

- **Feature Expansion:**  
  Continue to refine and add new features based on user feedback.

---

  ## Documentation & References

- **Django Documentation:** [https://docs.djangoproject.com/](https://docs.djangoproject.com/)
- **MySQL Documentation:** [https://dev.mysql.com/doc/](https://dev.mysql.com/doc/)
- **Bootstrap Framework:** [https://getbootstrap.com/](https://getbootstrap.com/)
- **Google Maps API:** [https://developers.google.com/maps](https://developers.google.com/maps)

---

## Contributing

Contributions are welcome! Please fork the repository and submit your pull requests. For major changes, open an issue first to discuss what you would like to change.

---

## License

Distributed under the MIT License. See the [LICENSE](LICENSE) file for more information.


---

## Getting Started

To set up the project locally:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/your-repository.git
