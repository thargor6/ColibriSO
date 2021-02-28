package com.overwhale.colibri_so.backend.repository;

import com.overwhale.colibri_so.backend.entity.SnippetIntent;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;

import javax.transaction.Transactional;
import java.util.UUID;

public interface SnippetIntentRepository extends JpaRepository<SnippetIntent, UUID> {

    @Transactional
    @Modifying
    @Query("DELETE FROM SnippetIntent i WHERE i.snippetId = ?1")
    void deleteBySnippetId(UUID uuid);
}
