package com.overwhale.colibri_so.domain.repository;

import com.overwhale.colibri_so.domain.entity.Project;
import com.overwhale.colibri_so.domain.entity.SnippetTag;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
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
