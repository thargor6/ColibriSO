package com.overwhale.colibri_so.domain.entity;

import com.fasterxml.jackson.annotation.JsonFormat;
import lombok.Data;
import org.hibernate.annotations.Type;

import javax.annotation.Nullable;
import javax.persistence.Entity;
import javax.persistence.EnumType;
import javax.persistence.Enumerated;
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
  @Nullable
  private UUID id;

  @Nullable
  @JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm:ss.SSSXXX")
  private OffsetDateTime creationTime;

  @Nullable
  @JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm:ss.SSSXXX")
  private OffsetDateTime lastChangedTime;

  @Nullable private UUID creatorId;

  @Nullable private String content;

  @Nullable private String description;

  @Enumerated(EnumType.STRING)
  @NotNull private SnippetType snippetType;

  @Nullable private String mimetype;

}
