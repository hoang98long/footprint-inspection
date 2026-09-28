"""Rigid 2D transformations: rotation and translation only, never scale."""

from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class RigidTransform:
    rotation: np.ndarray
    translation: np.ndarray

    @property
    def angle_degrees(self) -> float:
        return float(np.degrees(np.arctan2(self.rotation[1, 0], self.rotation[0, 0])))

    def apply(self, points: np.ndarray) -> np.ndarray:
        return points @ self.rotation.T + self.translation

    def inverse(self) -> "RigidTransform":
        inverse_rotation = self.rotation.T
        return RigidTransform(inverse_rotation, -self.translation @ inverse_rotation.T)

    def compose(self, prior: "RigidTransform") -> "RigidTransform":
        """Return this transform applied after ``prior``."""
        return RigidTransform(self.rotation @ prior.rotation, self.rotation @ prior.translation + self.translation)


IDENTITY_TRANSFORM = RigidTransform(np.eye(2, dtype=float), np.zeros(2, dtype=float))


def make_rotation(angle_radians: float) -> np.ndarray:
    cosine, sine = np.cos(angle_radians), np.sin(angle_radians)
    return np.array([[cosine, -sine], [sine, cosine]], dtype=float)


def estimate_rigid_transform(source: np.ndarray, target: np.ndarray) -> RigidTransform:
    """Kabsch estimate mapping matched source rows to target rows without scaling."""
    if len(source) < 3 or len(source) != len(target):
        raise ValueError("At least three paired source and target points are required.")
    source_center = source.mean(axis=0)
    target_center = target.mean(axis=0)
    covariance = (source - source_center).T @ (target - target_center)
    left, _, right_t = np.linalg.svd(covariance)
    rotation = right_t.T @ left.T
    if np.linalg.det(rotation) < 0:
        right_t[-1] *= -1
        rotation = right_t.T @ left.T
    return RigidTransform(rotation, target_center - rotation @ source_center)
