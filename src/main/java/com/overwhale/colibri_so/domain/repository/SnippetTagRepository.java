package com.overwhale.colibri_so.domain.repository;

import com.overwhale.colibri_so.domain.entity.SnippetTag;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.UUID;

public interface SnippetTagRepository extends JpaRepository<SnippetTag, UUID> {}
