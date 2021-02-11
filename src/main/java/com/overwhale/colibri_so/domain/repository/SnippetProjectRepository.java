package com.overwhale.colibri_so.domain.repository;

import com.overwhale.colibri_so.domain.entity.SnippetProject;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.UUID;

public interface SnippetProjectRepository extends JpaRepository<SnippetProject, UUID> {}
