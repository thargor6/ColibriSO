package com.overwhale.colibri_so.backend.repository;

import com.overwhale.colibri_so.backend.entity.Intent;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.UUID;

public interface IntentRepository extends JpaRepository<Intent, UUID> {}
