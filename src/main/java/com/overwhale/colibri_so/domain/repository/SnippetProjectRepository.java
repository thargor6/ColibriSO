package com.overwhale.colibri_so.domain.repository;

import com.overwhale.colibri_so.domain.entity.SnippetProject;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;

import javax.transaction.Transactional;
import java.util.UUID;

public interface SnippetProjectRepository extends JpaRepository<SnippetProject, UUID> {

    @Transactional
    @Modifying
    @Query("DELETE FROM SnippetProject p WHERE p.snippetId = ?1")
    void deleteBySnippetId(UUID uuid);
}
