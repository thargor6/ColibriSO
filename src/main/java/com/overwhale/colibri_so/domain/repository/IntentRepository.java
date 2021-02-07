package com.overwhale.colibri_so.domain.repository;

import com.overwhale.colibri_so.domain.entity.Intent;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.UUID;

public interface IntentRepository extends JpaRepository<Intent, UUID> {}
