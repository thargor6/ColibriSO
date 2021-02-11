package com.overwhale.colibri_so.domain.repository;

import com.overwhale.colibri_so.domain.entity.Snippet;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import java.util.UUID;

public interface SnippetRepository extends JpaRepository<Snippet, UUID> {

    @Query("SELECT count(s) FROM Snippet s, SnippetProject p WHERE p.projectId = ?1 AND p.snippetId = s.id")
    long countForProjectId(UUID projectId);

    @Query("SELECT s FROM Snippet s, SnippetProject p WHERE p.projectId = ?1 AND p.snippetId = s.id")
    Page<Snippet> findForProjectId(UUID projectId, Pageable pageable);

}
