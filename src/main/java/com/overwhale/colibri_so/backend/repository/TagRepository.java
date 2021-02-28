package com.overwhale.colibri_so.backend.repository;

import com.overwhale.colibri_so.backend.entity.Tag;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.UUID;

public interface TagRepository extends JpaRepository<Tag, UUID> {}
