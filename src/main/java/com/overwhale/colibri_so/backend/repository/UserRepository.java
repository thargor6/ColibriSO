package com.overwhale.colibri_so.backend.repository;

import com.overwhale.colibri_so.backend.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.UUID;

public interface UserRepository extends JpaRepository<User, UUID> {

  User getByUsername(String username);
}
