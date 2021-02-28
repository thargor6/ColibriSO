package com.overwhale.colibri_so.backend.entity;

import lombok.Data;
import org.hibernate.annotations.Type;

import javax.annotation.Nullable;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.IdClass;
import javax.persistence.Table;
import java.util.UUID;

@Entity
@Data
@Table(name = "snippet_tags")
@IdClass(SnippetTagKey.class)
public class SnippetTag {
  // TODO: create dtos for editing, so that the entities can have the appropriate NotNull-settings
  // for key-fields
  @Nullable
  @Id
  @Type(type = "uuid-char")
  private UUID snippetId;

  @Nullable
  @Id
  @Type(type = "uuid-char")
  private UUID tagId;
}
