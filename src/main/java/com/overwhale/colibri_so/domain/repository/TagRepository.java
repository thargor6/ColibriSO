package com.overwhale.colibri_so.domain.repository;

import com.overwhale.colibri_so.domain.entity.Tag;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.UUID;

public interface TagRepository extends JpaRepository<Tag, UUID> {
}
