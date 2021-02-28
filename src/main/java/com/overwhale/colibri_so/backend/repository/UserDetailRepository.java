package com.overwhale.colibri_so.backend.repository;

import com.overwhale.colibri_so.backend.entity.UserDetail;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.UUID;

public interface UserDetailRepository extends JpaRepository<UserDetail, UUID> {}
