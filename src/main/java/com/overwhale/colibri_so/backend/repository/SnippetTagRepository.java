package com.overwhale.colibri_so.backend.repository;

import com.overwhale.colibri_so.backend.entity.SnippetTag;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;

import javax.transaction.Transactional;
import java.util.UUID;

public interface SnippetTagRepository extends JpaRepository<SnippetTag, UUID> {

    @Transactional
    @Modifying
    @Query("DELETE FROM SnippetTag t WHERE t.snippetId = ?1")
    void deleteBySnippetId(UUID uuid);
}
