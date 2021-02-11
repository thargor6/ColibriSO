package com.overwhale.colibri_so.domain.repository;

import com.overwhale.colibri_so.domain.entity.SnippetIntent;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.UUID;

public interface SnippetIntentRepository extends JpaRepository<SnippetIntent, UUID> {}
