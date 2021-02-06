package com.overwhale.colibri_so.domain.entity;

import lombok.Data;
import org.hibernate.annotations.Type;

import javax.annotation.Nullable;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Table;
import javax.validation.constraints.NotNull;
import java.time.OffsetDateTime;
import java.util.UUID;

@Entity
@Data
@Table(name = "snippets")
public class Snippet {
  @Id
  @Type(type = "uuid-char")
  @NotNull
  private UUID id;

  @NotNull
  private OffsetDateTime creationTime;

  @Nullable
  private OffsetDateTime lastChangedTime;

  @NotNull
  private UUID creatorId;

  @Nullable
  private String description;

  @Nullable
  private String content;
}
