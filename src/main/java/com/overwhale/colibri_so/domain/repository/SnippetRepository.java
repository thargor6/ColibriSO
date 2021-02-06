package com.overwhale.colibri_so.domain.repository;

import com.overwhale.colibri_so.domain.entity.Snippet;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.UUID;

public interface SnippetRepository extends JpaRepository<Snippet, UUID> {
}
