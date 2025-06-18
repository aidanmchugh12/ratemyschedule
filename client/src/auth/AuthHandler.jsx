import { useAuth0 } from "@auth0/auth0-react";
import { useEffect } from "react";

const AuthHandler = () => {
  const { isAuthenticated, user, isLoading } = useAuth0();

  useEffect(() => {
    const addUserToDatabase = async () => {
      try {
        const response = await fetch("http://127.0.0.1:5000/api/add-user", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            sub: user.sub,
            name: user.name,
            email: user.email,
            created_at: user.created_at,
          }),
        });

        const result = await response.json();
        console.log(result.message);
      } catch (error) {
        console.error("Error adding user to database:", error);
      }
    };

    const userInDatabase = async () => {
      try {
        const response = await fetch("http://127.0.0.1:5000/api/check-user", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            sub: user.sub,
          }),
        });

        const result = await response.json();

        if (result.exists) {
          return true;
        } else {
          return false;
        }
      } catch (error) {
        console.error("Error checking user:", error);
        return false;
      }
    };

    const handleUser = async () => {
      if (!isLoading && isAuthenticated && user) {
        const exists = await userInDatabase();

        if (!exists) {
          addUserToDatabase();
        }
      }
    };

    handleUser();
  }, [isAuthenticated, user, isLoading]);

  return null;
};

export default AuthHandler;
