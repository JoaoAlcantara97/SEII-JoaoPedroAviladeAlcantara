import numpy as np
import matplotlib.pyplot as plt
import pygame
import sys

def draw_system(phi, theta):
    window.fill((255, 255, 255))  # Clear the window

    # Draw the cart
    cart_x = int(WINDOW_WIDTH / 2)
    cart_y = int(WINDOW_HEIGHT / 2)
    pygame.draw.rect(window, (0, 0, 0), (cart_x - CART_WIDTH/2, cart_y - CART_HEIGHT/2, CART_WIDTH, CART_HEIGHT))

    # Calculate the pendulum tip position
    pendulum_tip_x = int(cart_x + PENDULUM_LENGTH * np.sin(phi))
    pendulum_tip_y = int(cart_y - PENDULUM_LENGTH * np.cos(phi))  # Flip the y-coordinate

    # Calculate the reaction wheel position
    wheel_length = 20
    wheel_x = int(pendulum_tip_x + wheel_length * np.sin(theta))
    wheel_y = int(pendulum_tip_y - wheel_length * np.cos(theta))  # Flip the y-coordinate

    # Draw the pendulum
    pygame.draw.line(window, (0, 0, 0), (cart_x, cart_y), (pendulum_tip_x, pendulum_tip_y), PENDULUM_WIDTH)

    # Draw the reaction wheel
    pygame.draw.circle(window, (255, 255, 0), (int(pendulum_tip_x), int(pendulum_tip_y)), 20)
    pygame.draw.circle(window, (0, 0, 255), (wheel_x, wheel_y), 10)

    # Draw the target
    target_x = int(cart_x + PENDULUM_LENGTH * np.sin(target_phi))
    target_y = int(cart_y - PENDULUM_LENGTH * np.cos(target_phi))  # Flip the y-coordinate
    pygame.draw.circle(window, (255, 0, 0), (target_x, target_y), 10)

    # Draw the angles
    font = pygame.font.SysFont(None, 30)
    phi_text = font.render(f"Phi: {np.degrees(phi):.2f}", True, (0, 0, 0))
    theta_text = font.render(f"Theta: {np.degrees(theta):.2f}", True, (0, 0, 0))
    window.blit(phi_text, (10, 10))
    window.blit(theta_text, (10, 40))

    # Update the display
    pygame.display.update()



def complementary_filter(data, filtered_data, alpha):
    return alpha * filtered_data + (1 - alpha) * data

def simulate_system(a, b, c, phi0, phi_dot0, theta0, theta_dot0, dt, T, control_strategy, target_phi, target_theta, sensor_noise_std, filter_alpha):
    # Initialize time and arrays to store results
    t = np.arange(0, T, dt)
    phi = np.zeros_like(t)
    phi_dot = np.zeros_like(t)
    theta = np.zeros_like(t)
    theta_dot = np.zeros_like(t)
    
    # Set initial conditions
    phi[0] = phi0
    phi_dot[0] = phi_dot0
    theta[0] = theta0
    theta_dot[0] = theta_dot0
    
    # PID controller variables
    integral_error_phi = 0.0
    integral_error_theta = 0.0
    prev_error_phi = 0.0
    prev_error_theta = 0.0
    
    # Filter variables
    filtered_phi = phi[0]
    filtered_theta = theta[0]
    
    # Simulation loop
    for i in range(1, len(t)):
        # Calculate errors
        error_phi = target_phi - phi[i-1]
        error_theta = target_theta - theta[i-1]
        
        # Calculate control input using PID control
        u = control_strategy(error_phi, error_theta, dt, integral_error_phi, integral_error_theta, prev_error_phi, prev_error_theta)
        
        # Calculate the second derivatives
        phi_double_dot = a * np.sin(phi[i-1]) - b * u
        theta_double_dot = c * u
        
        # Update phi, phi_dot, theta, theta_dot using Euler's method
        phi[i] = phi[i-1] + dt * phi_dot[i-1]
        phi_dot[i] = phi_dot[i-1] + dt * phi_double_dot
        theta[i] = theta[i-1] + dt * theta_dot[i-1]
        theta_dot[i] = theta_dot[i-1] + dt * theta_double_dot
        
        # Add sensor noise to measurements
        noisy_phi = phi[i] + np.random.normal(0, sensor_noise_std)
        noisy_theta = theta[i] + np.random.normal(0, sensor_noise_std)
        
        # Apply complementary filter
        filtered_phi = complementary_filter(noisy_phi, filtered_phi, filter_alpha)
        filtered_theta = complementary_filter(noisy_theta, filtered_theta, filter_alpha)
        
        # Update measurements with filtered values
        phi[i] = filtered_phi
        theta[i] = filtered_theta
        
        # Update integral and previous errors for PID controller
        integral_error_phi += error_phi * dt
        integral_error_theta += error_theta * dt
        prev_error_phi = error_phi
        prev_error_theta = error_theta

        # Draw the system
        draw_system(phi[i], theta[i])
        clock.tick(100)
    
    return t, phi, phi_dot, theta, theta_dot

# Control strategy (PID controller)
def pid_controller(error_phi, error_theta, dt, integral_error_phi, integral_error_theta, prev_error_phi, prev_error_theta):
    # Constants for the controller
    Kp_phi = 15  # Proportional gain for phi control
    Ki_phi = 8  # Integral gain for phi control
    Kd_phi = 10  # Derivative gain for phi control
    Kp_theta =0.5  # Proportional gain for theta control
    Ki_theta = 0.2  # Integral gain for theta control
    Kd_theta = 0.1  # Derivative gain for theta control

    # Control input calculation
    proportional_term_phi = Kp_phi * error_phi
    integral_term_phi = Ki_phi * integral_error_phi
    derivative_term_phi = Kd_phi * (error_phi - prev_error_phi) / dt

    proportional_term_theta = Kp_theta * error_theta
    integral_term_theta = Ki_theta * integral_error_theta
    derivative_term_theta = Kd_theta * (error_theta - prev_error_theta) / dt

    u = -(proportional_term_phi + integral_term_phi + derivative_term_phi) - (proportional_term_theta + integral_term_theta + derivative_term_theta)

    return u

# Parameters
a = 1.0
b = 0.5
c = 2.0
phi0 = 0.7
phi_dot0 = 0.0
theta0 = 0
theta_dot0 = 0.0
dt = 0.01
T = 100.0
target_phi = 0
target_theta = 0.3
sensor_noise_std = 0.01  # Standard deviation of sensor noise
filter_alpha = 0.8  # Alpha value for the complementary filter

# Pygame parameters
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PENDULUM_LENGTH = 150
PENDULUM_WIDTH = 5
CART_WIDTH = 80
CART_HEIGHT = 40

pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Inverted Pendulum Simulation")

# Simulate the system
t, phi, phi_dot, theta, theta_dot = simulate_system(a, b, c, phi0, phi_dot0, theta0, theta_dot0, dt, T, pid_controller, target_phi, target_theta, sensor_noise_std, filter_alpha)


pygame.quit()
sys.exit()

# Plot the results
plt.figure()
plt.subplot(2, 1, 1)
plt.plot(t, phi, label='Phi')
plt.plot(t, phi_dot, label='Phi_dot')
plt.axhline(y=target_phi, color='r', linestyle='--', label='Target Phi')
plt.xlabel('Time')
plt.ylabel('Phi / Phi_dot')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(t, theta, label='Theta')
plt.plot(t, theta_dot, label='Theta_dot')
plt.axhline(y=target_theta, color='r', linestyle='--', label='Target Theta')
plt.xlabel('Time')
plt.ylabel('Theta / Theta_dot')
plt.legend()

plt.tight_layout()
plt.show()

