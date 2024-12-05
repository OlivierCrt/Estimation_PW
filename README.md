# Simulated Study of Robot Localization in a Map

## Overview

This project aims to illustrate basic stochastic estimation techniques through a simulated study of static 2D localization in robotics. The goal is to estimate the absolute position of a robot within a given map containing known landmarks.

### Context
- **World**: A 2D plane with a reference frame \( F_0 = (O, \vec{x_0}, \vec{y_0}) \), where \( \vec{x_0} \) and \( \vec{y_0} \) point East and North, respectively.
- **Landmarks**: \( M_1, M_2, ..., M_L \), with known absolute positions \( m_l = (u_l, v_l)^T \).
- **Robot**: A point-like entity with an unknown absolute position \( x = (u, v)^T \).
- **Observations**: Relative measurements \( z_l \) of each landmark \( M_l \) from the robot, combined into \( z = (z_1^T, ..., z_L^T)^T \).

## Problem Formulation

1. **Measurement Model**:
   - \( Z = h(x) + V \), where:
     - \( h(.) \) is the measurement function.
     - \( V \sim G(\bar{v}, C_v) \) is the Gaussian noise with mean \( \bar{v} \) and covariance \( C_v \).
   - \( h(x) = (h_1(x), ..., h_L(x))^T \), with \( h_l(x) = m_l - x \).

2. **Objective**:
   - Estimate the robot's position \( x \) from the observation vector \( z \).

## Provided Tools

- **`simulationDonnees.m`**:
  - Simulates an experiment by generating:
    - Measurement vector \( Z \).
    - Landmark positions.
    - Mean and covariance of the noise.
    - Hidden true position \( x \).
  - Allows visualizations when `plot_p = 1`.

- **`ellipse.m`**:
  - Plots the 99% confidence ellipse for a 2D Gaussian random variable with given mean and covariance.

## Tasks

### Case Study 1: Linear Measurement Function with IID Gaussian Noise

#### Model
- \( h(x) \): Affine function.
- Noise:
  - Mean \( \bar{v} = 0 \).
  - Covariance \( C_v = \sigma^2 I \), with \( \sigma \) provided.

#### Steps
1. **Simulations**:
   - Execute \( N \) experiments by invoking `simulationDonnees.m` and store the \( Z \) samples.
   - Note the value of \( \sigma \).

2. **Visualizations**:
   - Empirical distributions of sub-vectors \( Z_l \).
   - Compare empirical distributions to theoretical Gaussian distributions.

## How to Run

1. Clone the repository and load the MATLAB files.
2. Run `simulationDonnees.m` with different `cas_d_etude` values to explore various setups.
3. Use `ellipse.m` for visualizing confidence regions.

## Requirements

- MATLAB with standard libraries.

## Acknowledgments

This project was conducted as part of the **2ASRI Practical Work at Université Toulouse III Paul Sabatier - UPSSITECH**.
