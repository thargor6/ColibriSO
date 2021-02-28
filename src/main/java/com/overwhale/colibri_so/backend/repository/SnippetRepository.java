package com.overwhale.colibri_so.backend.repository;

import com.overwhale.colibri_so.backend.entity.Intent;
import com.overwhale.colibri_so.backend.entity.Project;
import com.overwhale.colibri_so.backend.entity.Snippet;
import com.overwhale.colibri_so.backend.entity.Tag;
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

    @Query("SELECT i FROM Intent i, SnippetIntent s WHERE s.snippetId = ?1 AND s.intentId = i.id")
    Page<Intent> findIntentsForSnippet(UUID snippetId, Pageable pageable);

    @Query("SELECT t FROM Tag t, SnippetTag s WHERE s.snippetId = ?1 AND s.tagId = t.id")
    Page<Tag> findTagsForSnippet(UUID snippetId, Pageable pageable);

    @Query("SELECT p FROM Project p, SnippetProject s WHERE s.snippetId = ?1 AND s.projectId = p.id")
    Page<Project> findProjectsForSnippet(UUID snippetId, Pageable pageable);
}
