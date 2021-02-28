package com.overwhale.colibri_so.backend.repository;

import com.overwhale.colibri_so.backend.entity.Project;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.UUID;

public interface ProjectRepository extends JpaRepository<Project, UUID> {}
